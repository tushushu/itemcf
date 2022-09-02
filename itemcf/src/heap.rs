use ordered_float::NotNan;
use std::cmp::Ordering;
use std::cmp::Reverse;
use std::collections::BinaryHeap;

// Key is item ID, and value is item score.
#[derive(Debug, Clone)]
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
    heap: BinaryHeap<Reverse<ItemScore>>,
    _size: usize,
    max_size: usize,
}

impl MinHeap {
    pub fn new(max_size: usize) -> MinHeap {
        MinHeap {
            heap: BinaryHeap::with_capacity(max_size),
            _size: 0,
            max_size: max_size,
        }
    }

    pub fn size(&self) -> usize {
        self._size
    }

    pub fn push(&mut self, elem: ItemScore) {
        let elem_r = Reverse(elem);
        let heap = &mut self.heap;
        if self._size == self.max_size {
            if elem_r < *heap.peek().unwrap() {
                heap.push(elem_r);
                heap.pop();
            }
        } else {
            heap.push(elem_r);
            self._size += 1;
        }
    }

    pub fn to_vec(&self) -> Vec<ItemScore> {
        vec![]
    }

    pub fn keys(&self) -> Vec<u32> {
        let result: Vec<u32> = self.heap.iter().map(|x| x.0 .0).collect();
        result
    }

    pub fn values(&self) -> Vec<NotNan<f32>> {
        let result: Vec<NotNan<f32>> = self.heap.iter().map(|x| x.0 .1).collect();
        result
    }

    fn peek(&self) -> ItemScore {
        (*self.heap.peek().unwrap()).0.clone()
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
