"""
Module Data Structures untuk Sistem Perpustakaan Digital
Mengimplementasikan 6+ struktur data yang diperlukan
"""

from abc import ABC, abstractmethod
from typing import Any, List, Tuple, Optional, Dict, Set
from collections import defaultdict
import json


class Node:
    """Node untuk Binary Search Tree (BST)"""
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class BinarySearchTree:
    """
    Binary Search Tree Implementation
    Digunakan untuk manajemen data buku berdasarkan ID atau ISBN
    """
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key: Any, value: Any) -> bool:
        """Insert key-value pair ke dalam BST"""
        if self.root is None:
            self.root = Node(key, value)
            self.size += 1
            return True
        else:
            return self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node: Node, key: Any, value: Any) -> bool:
        if key < node.key:
            if node.left is None:
                node.left = Node(key, value)
                self.size += 1
                return True
            return self._insert_recursive(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key, value)
                self.size += 1
                return True
            return self._insert_recursive(node.right, key, value)
        else:
            # Key sudah ada, update value
            node.value = value
            return False

    def search(self, key: Any) -> Optional[Any]:
        """Cari value berdasarkan key"""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node: Optional[Node], key: Any) -> Optional[Any]:
        if node is None:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def delete(self, key: Any) -> bool:
        """Hapus node dengan key tertentu"""
        old_size = self.size
        self.root = self._delete_recursive(self.root, key)
        return self.size < old_size

    def _delete_recursive(self, node: Optional[Node], key: Any) -> Optional[Node]:
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            self.size -= 1
            # Node dengan satu child atau tanpa child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node dengan dua child
            min_larger_node = self._find_min(node.right)
            node.key = min_larger_node.key
            node.value = min_larger_node.value
            node.right = self._delete_recursive(node.right, min_larger_node.key)

        return node

    def _find_min(self, node: Node) -> Node:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self) -> List[Tuple[Any, Any]]:
        """Traversal inorder menghasilkan list sorted berdasarkan key"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: Optional[Node], result: List):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.value))
            self._inorder_recursive(node.right, result)

    def get_all(self) -> List[Tuple[Any, Any]]:
        """Get semua data"""
        return self.inorder_traversal()


class HashTable:
    """
    Hash Table dengan chaining
    Digunakan untuk manajemen user dan indexing buku
    """
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]
        self.size = 0

    def _hash(self, key: str) -> int:
        """Simple hash function"""
        hash_value = 0
        for char in str(key):
            hash_value = (hash_value * 31 + ord(char)) % self.capacity
        return hash_value

    def insert(self, key: str, value: Any) -> None:
        """Insert key-value pair"""
        index = self._hash(key)
        
        # Check if key already exists
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        
        # Add new pair
        self.table[index].append((key, value))
        self.size += 1

    def search(self, key: str) -> Optional[Any]:
        """Search value berdasarkan key"""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key: str) -> bool:
        """Delete key-value pair"""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index].pop(i)
                self.size -= 1
                return True
        return False

    def get_all(self) -> Dict[str, Any]:
        """Get semua data sebagai dictionary"""
        result = {}
        for bucket in self.table:
            for key, value in bucket:
                result[key] = value
        return result

    def keys(self) -> List[str]:
        """Get semua keys"""
        result = []
        for bucket in self.table:
            for key, value in bucket:
                result.append(key)
        return result

    def values(self) -> List[Any]:
        """Get semua values"""
        result = []
        for bucket in self.table:
            for key, value in bucket:
                result.append(value)
        return result


class Queue:
    """
    Queue (FIFO) Implementation
    Digunakan untuk riwayat transaksi peminjaman
    """
    def __init__(self):
        self.items = []

    def enqueue(self, item: Any) -> None:
        """Add item ke belakang queue"""
        self.items.append(item)

    def dequeue(self) -> Optional[Any]:
        """Remove dan return item dari depan queue"""
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def peek(self) -> Optional[Any]:
        """View item paling depan tanpa menghapus"""
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self) -> bool:
        """Check apakah queue kosong"""
        return len(self.items) == 0

    def size(self) -> int:
        """Get ukuran queue"""
        return len(self.items)

    def get_all(self) -> List[Any]:
        """Get semua items"""
        return self.items.copy()


class Stack:
    """
    Stack (LIFO) Implementation
    Digunakan untuk tracking history operasi dan undo/redo
    """
    def __init__(self):
        self.items = []

    def push(self, item: Any) -> None:
        """Add item ke top stack"""
        self.items.append(item)

    def pop(self) -> Optional[Any]:
        """Remove dan return item dari top"""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self) -> Optional[Any]:
        """View top item tanpa menghapus"""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self) -> bool:
        """Check apakah stack kosong"""
        return len(self.items) == 0

    def size(self) -> int:
        """Get ukuran stack"""
        return len(self.items)

    def get_all(self) -> List[Any]:
        """Get semua items"""
        return self.items.copy()


class GraphNode:
    """Node untuk Graph"""
    def __init__(self, book_id: str, title: str):
        self.book_id = book_id
        self.title = title
        self.neighbors = []  # List of (neighbor_node, weight)

    def add_edge(self, neighbor: 'GraphNode', weight: float = 1.0) -> None:
        """Add edge ke neighbor"""
        if neighbor not in [n[0] for n in self.neighbors]:
            self.neighbors.append((neighbor, weight))

    def remove_edge(self, neighbor: 'GraphNode') -> None:
        """Remove edge ke neighbor"""
        self.neighbors = [(n, w) for n, w in self.neighbors if n != neighbor]


class Graph:
    """
    Graph Implementation
    Digunakan untuk sistem rekomendasi berdasarkan hubungan antar buku
    """
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}

    def add_node(self, book_id: str, title: str) -> GraphNode:
        """Add node ke graph"""
        if book_id not in self.nodes:
            self.nodes[book_id] = GraphNode(book_id, title)
        return self.nodes[book_id]

    def add_edge(self, book_id1: str, book_id2: str, weight: float = 1.0) -> None:
        """Add edge antara dua buku"""
        if book_id1 in self.nodes and book_id2 in self.nodes:
            self.nodes[book_id1].add_edge(self.nodes[book_id2], weight)

    def get_recommendations(self, book_id: str, depth: int = 1) -> List[Tuple[str, float]]:
        """Get rekomendasi buku berdasarkan book similarity"""
        if book_id not in self.nodes:
            return []

        recommendations = []
        visited = set()
        
        def dfs(node: GraphNode, current_depth: int, weight: float = 1.0):
            if current_depth == 0:
                return
            
            for neighbor, edge_weight in node.neighbors:
                if neighbor.book_id not in visited:
                    visited.add(neighbor.book_id)
                    combined_weight = weight * edge_weight
                    recommendations.append((neighbor.book_id, combined_weight))
                    dfs(neighbor, current_depth - 1, combined_weight)

        dfs(self.nodes[book_id], depth)
        # Sort by weight (relevance) descending
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations


class LinkedListNode:
    """Node untuk Linked List"""
    def __init__(self, data: Any):
        self.data = data
        self.next = None


class LinkedList:
    """
    Linked List Implementation
    Digunakan untuk menyimpan daftar dengan flexible operations
    """
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data: Any) -> None:
        """Add item ke akhir list"""
        new_node = LinkedListNode(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1

    def insert_at(self, index: int, data: Any) -> bool:
        """Insert item di posisi tertentu"""
        if index < 0 or index > self.size:
            return False
        
        if index == 0:
            new_node = LinkedListNode(data)
            new_node.next = self.head
            self.head = new_node
            self.size += 1
            return True

        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        new_node = LinkedListNode(data)
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return True

    def remove_at(self, index: int) -> Optional[Any]:
        """Remove item di posisi tertentu"""
        if index < 0 or index >= self.size or self.head is None:
            return None

        if index == 0:
            data = self.head.data
            self.head = self.head.next
            self.size -= 1
            return data

        current = self.head
        for _ in range(index - 1):
            current = current.next

        data = current.next.data
        current.next = current.next.next
        self.size -= 1
        return data

    def get(self, index: int) -> Optional[Any]:
        """Get item di posisi tertentu"""
        if index < 0 or index >= self.size:
            return None

        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def get_all(self) -> List[Any]:
        """Get semua items"""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result


# Priority Queue menggunakan Min Heap (untuk waiting list dengan prioritas)
class MinHeap:
    """
    Min Heap Implementation
    Digunakan untuk managing reservation queue dengan prioritas
    """
    def __init__(self):
        self.heap = []

    def insert(self, item: Tuple[int, Any]) -> None:
        """Insert item (priority, data)"""
        self.heap.append(item)
        self._bubble_up(len(self.heap) - 1)

    def extract_min(self) -> Optional[Tuple[int, Any]]:
        """Extract item dengan priority terendah"""
        if len(self.heap) == 0:
            return None
        
        min_item = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        if len(self.heap) > 0:
            self._bubble_down(0)
        
        return min_item

    def peek(self) -> Optional[Tuple[int, Any]]:
        """View min item tanpa extract"""
        if len(self.heap) > 0:
            return self.heap[0]
        return None

    def _bubble_up(self, index: int) -> None:
        """Move item up sampai heap property tercapai"""
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._bubble_up(parent_index)

    def _bubble_down(self, index: int) -> None:
        """Move item down sampai heap property tercapai"""
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if left_child < len(self.heap) and self.heap[left_child][0] < self.heap[smallest][0]:
            smallest = left_child

        if right_child < len(self.heap) and self.heap[right_child][0] < self.heap[smallest][0]:
            smallest = right_child

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._bubble_down(smallest)

    def size(self) -> int:
        """Get ukuran heap"""
        return len(self.heap)

    def is_empty(self) -> bool:
        """Check apakah heap kosong"""
        return len(self.heap) == 0

    def get_all(self) -> List[Tuple[int, Any]]:
        """Get semua items"""
        return self.heap.copy()
