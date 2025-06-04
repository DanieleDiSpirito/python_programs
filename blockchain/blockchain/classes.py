import random
from pydantic import conint, conbytes
from typing_extensions import Self, Optional, List, Union, Any, Set
import pickle  # from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError  # noqa (no pep8 warnings for this line)
from sortedcontainers import SortedSet
from Crypto.Util.number import bytes_to_long
from exceptions import AlreadyFullBlockException, InsufficientAmountException

NUM_NODES = 5
MAX_SIZE: conint(gt=0) = 10
TOT_AMOUNT: conint(gt=0) = 1000
POW_LENGTH: conint(ge=1) = 2


def deepcopy(obj: Any) -> Any:
    return pickle.loads(pickle.dumps(obj))


class Node:
    def __init__(self) -> None:
        key: SigningKey = SigningKey.generate(curve=SECP256k1)
        self.public_key: str = key.verifying_key.to_string().hex()
        self._private_key: SigningKey = key
        self.UTXO: SortedSet[TransactionOutput] = SortedSet()  # Unspent Transaction Outputs
        self.amount: conint(ge=0) = 0
        self.mempool: dict[str, Transaction | GenesisTransaction] = dict()
        self.nodes: dict[str, Node] = dict()
        self.neighbors: List[Node] = list()

    def make_transaction(self, receiver: Self, amount: conint(ge=1)) -> None:
        fee: conint(ge=2) = max(amount // 100, 2)  # 1% fee
        if self.amount < amount + fee:
            try:
                raise InsufficientAmountException(f"Unavailable amount ({amount}) for account {self}")
            except InsufficientAmountException as err:
                print(f"Error: {err}")
        used_utxo: List[TransactionOutput] = list()
        temp_amount: conint(ge=0) = 0
        for utxo in self.UTXO:
            if utxo.receiver == self.public_key:
                temp_amount += utxo.amount
                used_utxo.append(utxo)
                if temp_amount >= amount + fee:
                    break
            else:
                self.update_amount_for_not_own_txo(utxo)
        if temp_amount < amount + fee:
            self.amount = temp_amount
            try:
                raise InsufficientAmountException(f"Unavailable amount ({amount}) for account {self}")
            except InsufficientAmountException as err:
                print(f"Error: {err}")
        utxo_to_input: List[TransactionInput] = [TransactionInput(txo.tx_id, txo.vout, signature=self.sign(txo.tx_id + receiver.public_key)) for txo in used_utxo]
        tx: Transaction = Transaction(self, receiver, amount, utxo_to_input, fee)
        self.send_to_p2p_network(tx)
        self.add_to_mempool(tx)
        self.calc_mempool()

    def calc_mempool(self) -> None:
        tx: Transaction
        vout: conint(ge=0) = 0
        for tx_id, tx in self.mempool.items():
            if isinstance(tx, GenesisTransaction):
                continue
            input_amount: conint(ge=0) = 0
            for _input in tx.input:
                vk = VerifyingKey.from_string(bytes.fromhex(tx.sender.public_key), curve=SECP256k1)
                try:
                    vk.verify(_input.signature, (_input.tx_id + tx.receiver.public_key).encode())
                except BadSignatureError as err:
                    print(u'❌', f"Invalid transaction input!!! Error: {err}")
                    continue
                output: TransactionOutput = self.mempool.get(_input.tx_id).output[_input.vout]
                if output.receiver == tx.sender.public_key:
                    input_amount += output.amount
            if input_amount < tx.amount + tx.fee:
                try:
                    raise InsufficientAmountException("Insufficient Amount!")
                except InsufficientAmountException as err:
                    print(u'❌', f"Invalid transaction!!! Error: {err}")
            for _input in tx.input:
                vk = VerifyingKey.from_string(bytes.fromhex(tx.sender.public_key), curve=SECP256k1)
                try:
                    vk.verify(_input.signature, (_input.tx_id + tx.receiver.public_key).encode())
                except BadSignatureError:
                    continue
                output: TransactionOutput = self.mempool.get(_input.tx_id).output[_input.vout]
                if tx.sender.public_key != self.public_key:
                    self.nodes[tx.sender.public_key].update_amount_after_sending(output)
                else:
                    self.update_amount_after_sending(output)
            change: conint(ge=0) = input_amount - tx.amount - tx.fee
            if change != 0:
                change_output: TransactionOutput = TransactionOutput(tx_id, vout, tx.sender.public_key, change, False)
                vout += 1
                tx.output.append(change_output)
                if tx.sender.public_key != self.public_key:
                    self.nodes[tx.sender.public_key].update_amount(change_output)
                else:
                    self.update_amount(change_output)
            miner: Node = random.choice(list(self.nodes.values()))
            fee_output: TransactionOutput = TransactionOutput(tx_id, vout, miner.public_key, tx.fee, False)
            vout += 1
            tx.output.append(fee_output)
            if miner.public_key != self.public_key:
                self.nodes[miner.public_key].update_amount(fee_output)
            else:
                self.update_amount(fee_output)
            receiver_output: TransactionOutput = TransactionOutput(tx_id, vout, tx.receiver.public_key, tx.amount, False)
            vout += 1
            tx.output.append(receiver_output)
            if tx.receiver.public_key != self.public_key:
                self.nodes[tx.receiver.public_key].update_amount(receiver_output)
            else:
                self.update_amount(receiver_output)
            tx.output_count = vout
            print(tx.output)

    def sign(self, msg: Union[str, bytes]) -> bytes:
        if isinstance(msg, str):
            msg = msg.encode()
        return self._private_key.sign(msg)

    def update_amount(self, txo: "TransactionOutput") -> None:  # "TransactionOutput" forward declaration to not get error in circular dependencies
        if txo not in self.UTXO and txo.receiver == self.public_key:
            self.UTXO.add(txo)
            self.amount += txo.amount

    def update_amount_after_sending(self, used_txo: "TransactionOutput") -> None:  # "TransactionOutput" forward declaration to not get error in circular dependencies
        if used_txo in self.UTXO and used_txo.receiver == self.public_key:
            self.UTXO.remove(used_txo)
            self.amount -= used_txo.amount

    def update_amount_for_not_own_txo(self, txo: "TransactionOutput") -> None:
        if txo in self.UTXO:
            self.UTXO.remove(txo)
            self.amount -= txo.amount

    def send_to_p2p_network(self, tx: "Transaction") -> None:
        for neighbor in self.neighbors:
            neighbor.add_to_mempool(deepcopy(tx))

    def receive(self, txo_list: List["TransactionOutput"]) -> None:
        txo: TransactionOutput
        for txo in txo_list:
            if txo.receiver == self.public_key:
                self.update_amount(txo)
            else:
                self.nodes[txo.receiver].update_amount(txo)

    def add_to_mempool(self, tx: "Transaction") -> None:
        if tx.id in self.mempool:
            print(u'ℹ️', "Already received transaction!")
            return
        self.mempool[tx.id] = tx
        self.calc_mempool()

    def add_neighbors(self, neighbors: Set[Self]):
        for neighbor in neighbors:
            if neighbor is not self:
                self.neighbors.append(neighbor)

    def print_nodes(self) -> None:
        [print(node) for node in self.nodes]

    def __repr__(self) -> str:
        return f"({self.public_key}, {self.amount})"


class GenesisNode(Node):
    pass


@dataclass
class TransactionInput:
    tx_id: str
    vout: conint(ge=0)
    signature: bytes


@dataclass
class TransactionOutput:
    tx_id: str
    vout: conint(ge=0)
    receiver: str
    amount: conint(ge=0)
    used: bool = False

    def __lt__(self, other: Any):
        if not isinstance(other, TransactionOutput):
            raise Exception("Not a TXO")
        return self.amount < other.amount

    def __repr__(self) -> str:
        return ":".join([self.tx_id, str(self.vout), self.receiver, str(self.amount)])

    def __hash__(self) -> int:
        return bytes_to_long(Hash(msg=str(self)).bin)


class Transaction:
    def __init__(self, sender: Node, receiver: Node, amount: conint(gt=0), _input: List[TransactionInput], fee: conint(ge=2)) -> None:
        self.sender: Node = sender
        self.receiver: Node = receiver
        self.amount: conint(gt=0) = amount
        self.version: conbytes(min_length=4, max_length=4) = b'\x02\x00\x00\x00'
        self.input: List[TransactionInput] = _input
        self.input_count: conint(ge=1) = len(self.input)
        self.output: Optional[List[TransactionOutput]] = list()
        self.output_count: conint(ge=2, le=3) = 0  # receiver + fee + sender change (optional)
        self.fee: conint(ge=2) = fee
        self.valid: conint(ge=0) = 0
        self.id: str = Hash(msg=Hash(msg=str(self)).hex).hex

    def make_transaction(self) -> bool:
        assert not self.rejected
        if self.sender.amount < self.amount:
            self.reject()
            return False
        self.sender -= self.amount
        self.receiver += self.amount
        self.temp_approve()
        return True

    def temp_approve(self) -> None:
        assert not self.rejected
        self.done = True

    def reject(self) -> None:
        self.rejected = True
        self.done = False

    def __repr__(self) -> str:
        return f"['sender': {self.sender.public_key}, 'receiver': {self.receiver.public_key}, 'amount': {self.amount}, 'version': {self.version.decode()}, 'input': {self.input}]"

    def hash(self) -> str:
        return Hash(msg=str(self)).hex


class GenesisTransaction:
    def __init__(self, sender: Node, receivers: List[Node], amounts: List[conint(gt=0)]) -> None:
        self.sender: Node = sender
        self.receivers: List[Node] = receivers
        self.amounts: List[conint(gt=0)] = amounts
        self.output: Optional[List[TransactionOutput]] = list()
        self.id: str = '00' * 32

    def make_transactions(self) -> None:
        vout: conint(ge=0) = 0
        sender_money: conint(ge=0) = self.sender.amount
        for receiver, amount in zip(self.receivers, self.amounts):
            sender_money -= amount
            new_txo: TransactionOutput = TransactionOutput(self.id, vout, receiver.public_key, amount, False)
            self.output.append(new_txo)
            vout += 1
        self.sender.amount = 0  # no amount will be left


class Hash:
    def __init__(self, **kwargs: Union[str, bytes]) -> None:
        if kwargs.get("msg") is None:
            self.hex: Optional[str] = "00" * 32
            self.bin: Optional[conbytes(min_length=32, max_length=32)] = b'\x00' * 32
            return
        msg: Union[str, bytes, None] = kwargs.get("msg")
        bin_msg: bytes = msg.encode() if isinstance(msg, str) else msg
        _hash = sha256(bin_msg)
        self.hex: Optional[str] = _hash.hexdigest()
        self.bin: Optional[conbytes(min_length=32, max_length=32)] = _hash.digest()

    def null_block(self) -> None:
        self.hex = "00" * 32
        self.bin = b'\x00' * 32

    def __repr__(self) -> str:
        return self.hex


'''
class Node:
    def __init__(self) -> None:
        key: SigningKey = SigningKey.generate(curve=SECP256k1)
        self.public_key: str = key.verifying_key.to_string().hex()
        self._private_key: str = key.to_string().hex()
        self.UTXO: Set[TransactionOutput] = set()  # Unspent Transaction Outputs
        self.amount: confloat(ge=0) = 0.0

    def get_pub_key(self) -> str:
        return self.public_key

    def get_amount(self) -> confloat(ge=0):
        return self.amount

    def update_amount(self, *transactions: "TransactionOutput") -> None:  # "TransactionOutput" forward declaration to not get error in circular dependencies
        for tx in transactions:  # transaction when self earns
            if tx not in self.UTXO and tx.receiver == Hash(msg=self.public_key).hex:
                self.UTXO.add(tx)
                self.amount += tx.amount

    def update_amount_after_sending(self, *used_transactions: "TransactionOutput") -> None:  # "TransactionOutput" forward declaration to not get error in circular dependencies
        for tx in used_transactions:  # transaction when self spends
            if tx in self.UTXO and tx.receiver == Hash(msg=self.public_key).hex:
                self.UTXO.remove(tx)
                self.amount -= tx.amount

    def __repr__(self) -> str:
        return f"({str(self.public_key)}, {round(self.amount, 8)})"




class Block:
    def __init__(self, **kwargs) -> None:
        self.id: conint(ge=0) = kwargs.get("id") or 0
        self.transactions: Deque[Transaction] = deque()
        self.n_transaction: conint(ge=0) = 0
        self.max_size: conint(gt=0) = MAX_SIZE
        self.full: bool = False
        self.prev_hash: Hash = kwargs.get("prev_hash") or Hash()
        self.hash: Optional[Hash] = None
        self.approved: bool = False
        self.nonce: str = "00" * 16

    def add_transaction(self, transaction: Transaction) -> None:
        if self.is_full():
            raise AlreadyFullBlockException("This block is already full!")
        self.transactions.append(transaction)
        self.n_transaction += 1
        self.full = self.n_transaction == self.max_size

    def is_full(self) -> bool:
        return self.full

    def calc_hash(self) -> Hash:
        print(u"🎰", "Finding nonce...")
        while self.hash is None or not self.hash.hex.startswith("00" * POW_LENGTH):
            self.nonce = urandom(16).hex()
            self.hash = Hash(msg=str(self))
        print(u"👏", f"Nonce found: {self.nonce}")
        print(u"ℹ️", f"Block #{str(self.id).zfill(6)} hash: {self.hash.hex}")
        return self.hash

    def approve(self) -> None:
        self.approved = True

    def __repr__(self) -> str:
        _id: str = f"#{str(self.id).zfill(6)}"
        transactions: str = ":".join([transaction.hash() for transaction in self.transactions])
        n_transactions: str = str(self.n_transaction)
        max_size: str = str(self.max_size)
        nonce: str = self.nonce
        full: str = str(self.full)
        prev_hash: str = self.prev_hash.hex
        return "{" + ";".join([_id, transactions, n_transactions, max_size, nonce, full, prev_hash]) + "}"


def destroy_block(block: Block):
    del block


class Chain:
    def __init__(self) -> None:
        self.last_block: Block = Block()
        self.blocks: List[Block] = [self.last_block]
        self.nodes: Set[Node] = set()
        self.tot_amount = TOT_AMOUNT

    def gen_nodes(self, n: conint(gt=0)) -> None:
        self.nodes = set(Node(self.tot_amount / n) for _ in range(n))

    def gen_node(self) -> None:
        new_node: Node = Node()
        self.nodes.add(new_node)

    def get_nodes(self) -> Set[Node]:
        return self.nodes

    def valid_tot_amount(self) -> bool:
        tot_amount: confloat(ge=0) = 0
        for node in self.nodes:
            tot_amount += node.get_amount()
        tot_amount = round(tot_amount, 8)
        return tot_amount == self.tot_amount

    def update_last_block(self) -> None:
        if self.last_block.is_full():
            prev_block_hash: Hash = self.last_block.calc_hash()
            self.last_block.approve()
            print(u"👍", "Last block approved:", self.last_block)
            new_block: Block = Block(id=self.last_block.id + 1, prev_hash=prev_block_hash)
            self.blocks.append(new_block)
            self.last_block = self.blocks[-1]
            print(u"➕", "New block added:", self.last_block)

    def make_transaction(self) -> bool:
        try:
            s_r: List[Node] = random.sample(tuple(self.nodes), k=2)
            sender: Node = s_r[0]
            receiver: Node = s_r[1]
            amount = round((sender.get_amount() * 1.2) * random.random() + 0.002, 8)  # 0.002 -> min transaction amount
            transaction: Transaction = Transaction(sender, receiver, amount)
            valid: bool = transaction.make_transaction()
            self.update_last_block()
            self.last_block.add_transaction(transaction)
            if not valid:
                raise InsufficientAmountException(f"Unavailable amount ({amount}) for account {sender}")
        except Exception as err:
            print(u"⚠️", "Transaction rejected:", err)
            return False
        return self.valid_tot_amount()

    def make_transactions(self, n: conint(gt=0)) -> None:
        valid_transaction: conint(ge=0) = 0
        while valid_transaction < n:
            if not self.make_transaction():
                if self.last_block.n_transaction > 0:
                    last_transaction: Transaction = self.last_block.transactions.pop()
                    self.last_block.n_transaction -= 1
                    self.last_block.full = False
                    last_transaction.reject()
                    print(u"❌", last_transaction.hash(), last_transaction)
            else:
                valid_transaction += 1
                print(u"☑️", self.last_block.transactions[-1].hash(), self.last_block.transactions[-1])

    def show_nodes(self) -> None:
        print("======= BLOCKCHAIN NODES =======")
        for idx, node in enumerate(self.nodes):
            print(f"{idx+1}: {node}")

    def __repr__(self) -> str:
        return "->".join([str(block.hash) for block in self.blocks])


class Main:
    def __init__(self) -> None:
        self.genesisNode: Node = GenesisNode()
        self.nodes: Set[Node] = set()

    def gen_nodes(self, n: conint(gt=0)) -> None:
        self.nodes = set(Node() for _ in range(n))

    def gen_node(self) -> None:
        new_node: Node = Node()
        self.nodes.add(new_node)

    def get_nodes(self) -> Set[Node]:
        return self.nodes

    def valid_tot_amount(self) -> bool:
        tot_amount: confloat(ge=0) = 0
        for node in self.nodes:
            tot_amount += node.get_amount()
        tot_amount = round(tot_amount, 8)
        return tot_amount == self.tot_amount

    def update_last_block(self) -> None:
        if self.last_block.is_full():
            prev_block_hash: Hash = self.last_block.calc_hash()
            self.last_block.approve()
            print(u"👍", "Last block approved:", self.last_block)
            new_block: Block = Block(id=self.last_block.id + 1, prev_hash=prev_block_hash)
            self.blocks.append(new_block)
            self.last_block = self.blocks[-1]
            print(u"➕", "New block added:", self.last_block)

    def make_transaction(self) -> bool:
        try:
            s_r: List[Node] = random.sample(tuple(self.nodes), k=2)
            sender: Node = s_r[0]
            receiver: Node = s_r[1]
            amount = round((sender.get_amount() * 1.2) * random.random() + 0.002, 8)  # 0.002 -> min transaction amount
            transaction: Transaction = Transaction(sender, receiver, amount)
            valid: bool = transaction.make_transaction()
            self.update_last_block()
            self.last_block.add_transaction(transaction)
            if not valid:
                raise InsufficientAmountException(f"Unavailable amount ({amount}) for account {sender}")
        except Exception as err:
            print(u"⚠️", "Transaction rejected:", err)
            return False
        return self.valid_tot_amount()

    def make_transactions(self, n: conint(gt=0)) -> None:
        valid_transaction: conint(ge=0) = 0
        while valid_transaction < n:
            if not self.make_transaction():
                if self.last_block.n_transaction > 0:
                    last_transaction: Transaction = self.last_block.transactions.pop()
                    self.last_block.n_transaction -= 1
                    self.last_block.full = False
                    last_transaction.reject()
                    print(u"❌", last_transaction.hash(), last_transaction)
            else:
                valid_transaction += 1
                print(u"☑️", self.last_block.transactions[-1].hash(), self.last_block.transactions[-1])

    def show_nodes(self) -> None:
        print("======= BLOCKCHAIN NODES =======")
        for idx, node in enumerate(self.nodes):
            print(f"{idx+1}: {node}")

    def __repr__(self) -> str:
        return "->".join([str(block.hash) for block in self.blocks])
'''


class Main:
    def __init__(self) -> None:
        self.genesisNode: GenesisNode = GenesisNode()
        self.nodes: Set[Node] = set()

    def gen_nodes(self, n: conint(gt=0)) -> None:
        self.nodes = set(Node() for _ in range(n))
        for node in self.nodes:
            node.add_neighbors(self.nodes)  # automatically not include itself
            node.nodes = {n.public_key: deepcopy(n) for n in self.nodes if n.public_key != node.public_key}

    def start(self) -> None:
        self.gen_nodes(NUM_NODES)
        nodes_dict: dict[Node, int] = dict()
        for node in self.nodes:
            nodes_dict[node] = random.randint(0, TOT_AMOUNT // NUM_NODES)
        genesis_transaction: GenesisTransaction = GenesisTransaction(self.genesisNode, list(self.nodes), list(nodes_dict.values()))
        genesis_transaction.make_transactions()
        self.send_to_p2p_network_genesis(genesis_transaction)

    def send_to_p2p_network_genesis(self, genesis_tx: GenesisTransaction):
        for node in self.nodes:
            node.receive(genesis_tx.output)
            node.mempool[genesis_tx.id] = deepcopy(genesis_tx)

    def print_nodes(self) -> None:
        for node in self.nodes:
            print(f"Node: {node}")
            node.print_nodes()

    def make_transaction(self):
        sender: Node
        receiver: Node
        sender, receiver = random.sample(self.nodes, 2)
        amount: conint(ge=1) = random.randint(1, (sender.amount * 99) // 100 - 2)
        sender.make_transaction(receiver, amount)
