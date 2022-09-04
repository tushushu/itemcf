use ordered_float::NotNan;
use std::cmp::Ordering;
use std::mem;
use std::ops::Index;

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
    max_size: usize,
}

impl Index<usize> for MinHeap {
    type Output = ItemScore;

    fn index(&self, idx: usize) -> &Self::Output {
        &self._heap[idx]
    }
}

impl MinHeap {
    pub fn new(max_size: usize) -> MinHeap {
        MinHeap {
            _heap: Vec::with_capacity(max_size),
            _size: 0,
            max_size: max_size,
        }
    }

    pub fn len(&self) -> usize {
        self._size
    }

    pub fn push(&mut self, elem: ItemScore) {}

    fn _shift_up(&mut self, idx: usize) {
        assert!(
            idx < self._size,
            "Parameter idx must be less than heap size!"
        );
        let parent = (idx - 1) / 2;
        while parent >= 0 && self[parent] < self[idx] {
            mem::swap(&mut self._heap[parent], &mut self._heap[idx]);
            idx = parent;
            parent = (idx - 1) / 2;
        }
    }

    pub fn into_sorted_vec(&self) -> Vec<ItemScore> {
        self._heap.into_sorted_vec().iter().map(|x| x.0).collect()
    }

    pub fn keys(&self) -> Vec<u32> {
        self.to_vec().iter().map(|x| x.0).collect()
    }

    pub fn values(&self) -> Vec<NotNan<f32>> {
        let result: Vec<NotNan<f32>> = self._heap.iter().map(|x| x.0 .1).collect();
        result
    }

    fn peek(&self) -> ItemScore {
        (*self._heap.peek().unwrap()).0.clone()
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
    fn test_size() {
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
}
