fn min_cmp(a: (i32, f32), b: (i32, f32)) -> bool {
    return a.1 > b.1;
}

fn max_cmp(a: (i32, f32), b: (i32, f32)) -> bool {
    return a.1 < b.1;
}
