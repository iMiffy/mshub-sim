class pqueue:
    def __init__(self, key = 0):
        self.arr = []
        self.key = key
    
    def _finder(self, p):
        topIdx = len(self.arr)
        botIdx = -1
        midIdx = (topIdx + botIdx) // 2
        while botIdx != midIdx:
            if p < self.arr[midIdx][self.key]: topIdx = midIdx
            elif p > self.arr[midIdx][self.key]: botIdx = midIdx
            else: return midIdx
            midIdx = (topIdx + botIdx) // 2
        return botIdx # Insert after this

    def add(self, data):
        p = data[self.key]
        idx = self._finder(p)
        if idx >= 0 and p < self.arr[idx][self.key]: print("QUEUE ERROR@@@@@@!!!!!!!")
        self.arr = self.arr[:idx+1] + [ data ] + self.arr[idx+1:]
        
    def show(self, num = 5):
        print(f'Showing earliest sample {num}')
        print(f'arrivTime, TYPE, cellNum, callDuration, carSpeed, startPos, uniqID')
        for i in range(num):
            if i >= len(self.arr): break
            print(self.arr[i])

    def pop(self):
        return self.arr.pop(0)
    
