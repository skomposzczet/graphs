mod graph;
mod alg;

use std::fs::File;
use std::io::{BufRead, BufReader};
use clap::Parser;
use graph::{Point, Graph};
use alg::simulated_annealing;

#[derive(Debug, Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(help = "Input file containing coordinates")]
    filepath: String,

    #[arg(long, short, default_value_t = 200, help = "Cooldown iter")]
    cooldown: u32,

    #[arg(long, short, default_value_t = 400, help = "Max iter")]
    iter: u32,
}

fn main() {
    let args = Args::parse();
    println!("{:?}", args);

    let graph: Graph = {
        let file = File::open(args.filepath).unwrap();
        let data = BufReader::new(file)
            .lines()
            .map(|line| Point::from_str(&line.unwrap()))
            .collect();
        Graph::new(data)
    };
    simulated_annealing(&graph, args.cooldown, args.iter);
}
