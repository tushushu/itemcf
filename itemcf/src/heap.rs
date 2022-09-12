use ordered_float::NotNan;
use std::cmp::Ordering;
use std::ops::Index;
use std::ops::IndexMut;

// Key is item ID, and value is item score.
#[derive(Debug, Copy, Clone)]
struct ItemScore(u32, NotNan<f32>);

impl PartialEq for ItemScore {
    fn eq(&self, other: &ItemScore) -> bool {
        self.1 == other.1
    }
}

impl Eq for ItemScore {}

impl Ord for ItemScore {
    fn cmp(&self, other: &Self) -> Ordering {
        self.1.cmp(&other.1)
    }
}

impl PartialOrd for ItemScore {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl ItemScore {
    pub fn new(key: u32, val: f32) -> ItemScore {
        ItemScore(key, NotNan::new(val).unwrap())
    }
}

struct MinHeap {
    _heap: Vec<ItemScore>,
    _size: usize,
    _max_size: usize,
}

impl Index<usize> for MinHeap {
    type Output = ItemScore;

    fn index(&self, idx: usize) -> &Self::Output {
        &self._heap[idx]
    }
}

impl IndexMut<usize> for MinHeap {
    fn index_mut(&mut self, idx: usize) -> &mut Self::Output {
        &mut self._heap[idx]
    }
}

impl MinHeap {
    pub fn new(max_size: usize) -> MinHeap {
        MinHeap {
            _heap: Vec::with_capacity(max_size),
            _size: 0,
            _max_size: max_size,
        }
    }

    pub fn size(&self) -> usize {
        self._size
    }

    pub fn max_size(&self) -> usize {
        self._max_size
    }

    pub fn push(&mut self, elem: ItemScore) {
        if self._size == self._max_size {
            if elem > self._peek() {
                self[0] = elem;
                self._sift_down(0);
            }
        } else {
            self._heap.push(elem);
            self._size += 1;
            self._sift_up(self._size - 1);
        }
    }

    fn _sift_down(&mut self, mut idx: usize) {
        let mut child = (idx + 1) * 2 - 1;
        while child < self._size {
            if child + 1 < self._size && self[child + 1] < self[child] {
                child += 1;
            }
            if self[idx] > self[child] {
                self._heap.swap(idx, child);
                idx = child;
                child = (idx + 1) * 2 - 1;
            } else {
                break;
            }
        }
    }

    fn _sift_up(&mut self, mut idx: usize) {
        if idx == 0 {
            return;
        }
        assert!(
            idx < self._size,
            "Parameter idx must be less than the heap size!"
        );
        let mut parent = (idx - 1) / 2;
        while self[parent] > self[idx] {
            self._heap.swap(parent, idx);
            idx = parent;
            if idx == 0 {
                break;
            }
            parent = (idx - 1) / 2;
        }
    }

    fn _capacity(&self) -> usize {
        self._heap.capacity()
    }

    pub fn into_sorted_vec(&self) -> Vec<ItemScore> {
        vec![]
    }

    pub fn keys(&self) -> Vec<u32> {
        self._heap.iter().map(|x| x.0).collect()
    }

    pub fn values(&self) -> Vec<NotNan<f32>> {
        let result: Vec<NotNan<f32>> = self._heap.iter().map(|x| x.1).collect();
        result
    }

    fn _peek(&self) -> ItemScore {
        self[0]
    }
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn test_eq() {
        assert_eq!(ItemScore::new(0, 0.1), ItemScore::new(0, 0.1),);

        assert_eq!(ItemScore::new(0, 0.1), ItemScore::new(1, 0.1),);
    }

    #[test]
    fn test_ne() {
        assert_ne!(ItemScore::new(0, 0.1), ItemScore::new(1, 0.2),);

        assert_ne!(ItemScore::new(0, 0.1), ItemScore::new(0, 0.2),);
    }

    #[test]
    fn test_gt() {
        assert!(ItemScore::new(0, 0.2) > ItemScore::new(1, 0.1));
        assert!(ItemScore::new(1, 0.2) > ItemScore::new(0, 0.1));
    }

    #[test]
    fn test_lt() {
        assert!(ItemScore::new(0, 0.1) < ItemScore::new(1, 0.2));
        assert!(ItemScore::new(1, 0.1) < ItemScore::new(0, 0.2));
    }

    #[test]
    fn test_capacity() {
        let heap = MinHeap::new(3);
        assert_eq!(heap._capacity(), 3);
    }

    #[test]
    fn test_size() {
        let heap = MinHeap::new(3);
        assert_eq!(heap.size(), 0);
    }

    #[test]
    fn test_max_size() {
        let heap = MinHeap::new(3);
        assert_eq!(heap.max_size(), 3);
    }

    #[test]
    fn test_push() {
        let mut heap = MinHeap::new(5);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap.size(), 1);

        heap.push(ItemScore::new(2, 0.2));
        assert_eq!(heap.size(), 2);

        heap.push(ItemScore::new(3, 0.3));
        assert_eq!(heap.size(), 3);

        heap.push(ItemScore::new(4, 0.4));
        assert_eq!(heap.size(), 4);

        heap.push(ItemScore::new(5, 0.5));
        assert_eq!(heap.size(), 5);

        heap.push(ItemScore::new(6, 0.0));
        assert_eq!(heap.size(), 5);

        heap.push(ItemScore::new(7, 0.6));
        assert_eq!(heap.size(), 5);
    }

    #[test]
    fn test_peek() {
        // size = 1, ascending order
        let mut heap = MinHeap::new(1);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.2));
        assert_eq!(heap._peek().1, 0.2);

        // size = 1, descending order
        let mut heap = MinHeap::new(1);

        heap.push(ItemScore::new(1, 0.2));
        assert_eq!(heap._peek().1, 0.2);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap._peek().1, 0.2);

        // size = 2, ascending order
        let mut heap = MinHeap::new(2);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.2));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.3));
        assert_eq!(heap._peek().1, 0.2);

        // size = 2, descending order
        let mut heap = MinHeap::new(2);

        heap.push(ItemScore::new(1, 0.3));
        assert_eq!(heap._peek().1, 0.3);

        heap.push(ItemScore::new(1, 0.2));
        assert_eq!(heap._peek().1, 0.2);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap._peek().1, 0.2);

        // size = 3, ascending order
        let mut heap = MinHeap::new(3);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.2));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.3));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.4));
        assert_eq!(heap._peek().1, 0.2);

        // size = 3, descending order
        let mut heap = MinHeap::new(3);

        heap.push(ItemScore::new(1, 0.4));
        assert_eq!(heap._peek().1, 0.4);

        heap.push(ItemScore::new(1, 0.3));
        assert_eq!(heap._peek().1, 0.3);

        heap.push(ItemScore::new(1, 0.2));
        assert_eq!(heap._peek().1, 0.2);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap._peek().1, 0.2);

        // size = 4, ascending order
        let mut heap = MinHeap::new(4);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.2));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.3));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.4));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.5));
        assert_eq!(heap._peek().1, 0.2);

        // size = 4, descending order
        let mut heap = MinHeap::new(4);

        heap.push(ItemScore::new(1, 0.5));
        assert_eq!(heap._peek().1, 0.5);

        heap.push(ItemScore::new(1, 0.4));
        assert_eq!(heap._peek().1, 0.4);

        heap.push(ItemScore::new(1, 0.3));
        assert_eq!(heap._peek().1, 0.3);

        heap.push(ItemScore::new(1, 0.2));
        assert_eq!(heap._peek().1, 0.2);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap._peek().1, 0.2);

        // size = 5, ascending order
        let mut heap = MinHeap::new(5);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.2));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.3));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.4));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.5));
        assert_eq!(heap._peek().1, 0.1);

        heap.push(ItemScore::new(1, 0.6));
        assert_eq!(heap._peek().1, 0.2);

        // size = 5, descending order
        let mut heap = MinHeap::new(5);

        heap.push(ItemScore::new(1, 0.6));
        assert_eq!(heap._peek().1, 0.6);

        heap.push(ItemScore::new(1, 0.5));
        assert_eq!(heap._peek().1, 0.5);

        heap.push(ItemScore::new(1, 0.4));
        assert_eq!(heap._peek().1, 0.4);

        heap.push(ItemScore::new(1, 0.3));
        assert_eq!(heap._peek().1, 0.3);

        heap.push(ItemScore::new(1, 0.2));
        assert_eq!(heap._peek().1, 0.2);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap._peek().1, 0.2);
    }

    #[test]
    fn test_keys() {
        let mut heap = MinHeap::new(2);
        let v: Vec<u32> = vec![];
        assert_eq!(heap.keys(), v);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap.keys(), vec![1]);

        heap.push(ItemScore::new(2, 0.2));
        assert_eq!(heap.keys(), vec![1, 2]);
    }

    #[test]
    fn test_values() {
        let mut heap = MinHeap::new(2);
        let v: Vec<f32> = vec![];
        assert_eq!(heap.values(), v);

        heap.push(ItemScore::new(1, 0.1));
        assert_eq!(heap.values(), vec![0.1]);

        heap.push(ItemScore::new(2, 0.2));
        assert_eq!(heap.values(), vec![0.1, 0.2]);
    }
}
