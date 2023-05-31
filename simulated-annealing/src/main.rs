mod graph;
mod alg;

use std::fs::File;
use std::io::{BufRead, BufReader};
use graph::Point;

fn main() {
    let points: Vec<Point> = {
        let file = File::open("input.dat").unwrap();
        BufReader::new(file)
            .lines()
            .map(|line| Point::from_str(&line.unwrap()))
            .collect()
    };
}
