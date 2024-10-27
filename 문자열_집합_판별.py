import sys
from collections import deque

class Node:
    def __init__(self, data):
        self.data = data
        self.key = None
        self.next = {}
        self.fail = None

class AhoCorasick:
    def __init__(self):
        self.root = Node(None)
        self.num_nodes = 1

    def insert(self, word, index):
        current = self.root
        for char in word:
            if char not in current.next:
                current.next[char] = Node(char)
                self.num_nodes += 1
            current = current.next[char]
        current.key = index  # 노드에 패턴의 인덱스 저장

    # bfs 기반 실패 포인터 지정, 모든 노드 삽입 이후에 진행, 루트에서 시작
    def build_failure_pointers(self):
        queue = deque()
        for char, child in self.root.next.items():
            child.fail = self.root
            queue.append(child)

        while queue:
            current = queue.popleft()
            
            for char, child in current.next.items():
                queue.append(child)
                fail_state = current.fail
                while fail_state and char not in fail_state.next:
                    fail_state = fail_state.fail
                child.fail = fail_state.next[char] if fail_state else self.root

    def search(self, text):
        current = self.root
        results = []
        
        for i, char in enumerate(text):
            while current and char not in current.next:
                current = current.fail
            if current is None:
                current = self.root
                continue
            
            current = current.next[char]
            # 실패 포인터를 따라 올라가며 패턴 확인
            temp = current
            while temp:
                if temp.key is not None: 
                    # (매칭된 텍스트 인덱스, 패턴 인덱스)
                    results.append((i - len(patterns[temp.key]) + 1, temp.key)) 
                temp = temp.fail

        return results

n = int(sys.stdin.readline())
patterns = [sys.stdin.readline().rstrip() for _ in range(n)]

ac = AhoCorasick()
for index, pattern in enumerate(patterns):
    ac.insert(pattern, index)
ac.build_failure_pointers()

for _ in range(int(sys.stdin.readline())):
    parent = sys.stdin.readline().rstrip()
    res = ac.search(parent)
    print('YES' if res else 'NO')