use ordered_float::NotNan;
use std::cmp::Ordering;
use std::cmp::Reverse;
use std::collections::BinaryHeap;

// Key is item ID, and value is item score.
#[derive(Debug)]
struct ItemScore(i32, NotNan<f32>);

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
    pub fn new(key: i32, val: f32) -> ItemScore {
        ItemScore(key, NotNan::new(val).unwrap())
    }
}

struct MinHeap {
    heap: BinaryHeap<Reverse<ItemScore>>,
    size: usize,
    max_size: usize,
}

impl MinHeap {
    pub fn new(max_size: usize) -> MinHeap {
        MinHeap {
            heap: BinaryHeap::new(),
            size: 0,
            max_size: max_size,
        }
    }
}

trait FixedSize {
    fn push(&mut self, elem: ItemScore);
}

impl FixedSize for MinHeap {
    fn push(&mut self, elem: ItemScore) {
        let elem_r = Reverse(elem);
        let heap = &mut self.heap;
        if self.size == self.max_size {
            if elem_r < *heap.peek().unwrap() {
                heap.push(elem_r);
                heap.pop();
            }
        } else {
            heap.push(elem_r);
        }
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

    // #[test]
    // fn test_size() {
    //     let heap = MinHeap::new(5);
    // }
}
