mod graph;
mod alg;

use std::fs::File;
use std::io::{BufRead, BufReader};
use graph::{Point, Graph};
use alg::simulated_annealing;

fn main() {
    let graph: Graph = {
        let file = File::open("input.dat").unwrap();
        let data = BufReader::new(file)
            .lines()
            .map(|line| Point::from_str(&line.unwrap()))
            .collect();
        Graph::new(data)
    };
}
