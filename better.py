from collections import deque

C_SIZE = 26 # 알파벳은 26개 이므로
C_TO_I = lambda x: x - 97  # ASCII 'a' = 97이므로, 0~25의 인덱스로 변환

class Trie:
    def __init__(self):
        self.go = [None] * C_SIZE  # 다음 노드를 가리키는 배열
        self.fail = None            # 실패 시 돌아갈 노드
        self.output = False         # 이 노드가 패턴의 끝인지 여부

    def add(self, key):
        if not key:
            self.output = True  # 빈 키 추가 시 출력 플래그 설정
            return
        
        index = C_TO_I(key[0])  # 첫 번째 문자의 인덱스
        if self.go[index] is None:
            self.go[index] = Trie()  # 자식 노드가 없으면 새 노드 생성
        self.go[index].add(key[1:])  # 나머지 문자열 재귀적으로 추가

class AhoCorasick:
    def __init__(self, trie: Trie):
        self.trie = trie
        self.trie.fail = self.trie  # 루트 노드의 실패 포인터는 자기 자신
        
        # BFS를 통해 실패 포인터 설정
        queue = deque([self.trie])
        while queue:
            current_node = queue.popleft()
            for i in range(C_SIZE):
                child_node = current_node.go[i]
                if not child_node:
                    continue
                
                # 루트 노드 자식의 실패 포인터는 루트
                if current_node == self.trie:
                    child_node.fail = self.trie
                else:
                    fail_node = current_node.fail
                    # 실패 포인터를 따라가며 적절한 실패 노드 찾기
                    while fail_node != self.trie and not fail_node.go[i]:
                        fail_node = fail_node.fail
                    if fail_node.go[i]:
                        fail_node = fail_node.go[i]
                    child_node.fail = fail_node
                
                # 출력 플래그 상속
                child_node.output |= child_node.fail.output
                queue.append(child_node)

    def __contains__(self, s: str):
        current_node = self.trie
        for char in s:
            index = C_TO_I(char)  # 문자에 대한 인덱스
            
            # 현재 노드에서 해당 문자로 이동 가능할 때까지 실패 노드를 따라감
            while current_node != self.trie and not current_node.go[index]:
                current_node = current_node.fail
            
            if current_node.go[index]:
                current_node = current_node.go[index]  # 다음 노드로 이동
            
            # 출력 플래그가 설정된 경우 패턴이 발견된 것
            if current_node.output:
                return True
        return False


# 패턴을 Trie에 추가
N = int(input())
trie = Trie()
for _ in range(N):
    trie.add(input().rstrip())
ac = AhoCorasick(trie)
    
# 각 쿼리에 대해 결과를 확인
Q = int(input())
queries = [input().rstrip() for _ in range(Q)]
for query in queries:
    print("YES" if query in ac else "NO")