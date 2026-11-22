import bisect, hashlib

class HashRing:
    def __init__(self, replicas=32): self.replicas, self.keys, self.ring = replicas, [], {}
    def _h(self, s): return int(hashlib.sha256(s.encode()).hexdigest()[:16], 16)
    def add_node(self, node):
        for i in range(self.replicas):
            k = self._h(f"{node}#{i}"); self.ring[k] = node; bisect.insort(self.keys, k)
    def get_node(self, key):
        idx = bisect.bisect(self.keys, self._h(key)) % len(self.keys)
        return self.ring[self.keys[idx]]

if __name__ == "__main__":
    hr = HashRing(16)
    for n in ["node-a", "node-b", "node-c"]: hr.add_node(n)
    assert hr.get_node("user:101") in {"node-a", "node-b", "node-c"}
    print("[PASS] 031_consistent_hash_ring")
