use crate::graph::Graph;
use rand::{thread_rng, seq::SliceRandom, Rng};

pub fn simulated_annealing(graph: &Graph, cooldown_iter: u32, max_iter: u32) {
    println!("{}, {}", cooldown_iter, max_iter);
    let mut cycle: Vec<usize> =  (0..graph.len()).collect();
    cycle.shuffle(&mut thread_rng());
    println!("{}", calc_distance(graph, &cycle));
    for i in (1..cooldown_iter+1).rev() {
        let temperature: f32 = 0.001 * (i as f32).powi(2);

        for _ in 0..max_iter {
            let mut cycle_new = cycle.clone();
            swap_edges(&mut cycle_new, &random_edges(cycle.len()));

            let cur_dist = calc_distance(graph, &cycle);
            let new_dist = calc_distance(graph, &cycle_new);
            if new_dist < cur_dist {
                cycle = cycle_new;
            } else {
                let r = thread_rng().gen::<f32>();
                if r < f32::exp(-( (new_dist - cur_dist) / temperature)) {
                    cycle = cycle_new;
                }
            }
        }
    }
    println!("{}", calc_distance(graph, &cycle));
}

fn calc_distance(graph: &Graph, cycle: &[usize])-> f32 {
    let mut sum: f32 = 0.0;
    let mut prev_point = cycle[0];
    cycle.iter().for_each(|curr_point| {
        sum += graph[*curr_point].distance(&graph[prev_point]);
        prev_point = *curr_point;
    }); 
    
    return sum + graph[cycle[0]].distance(&graph[prev_point]);
}

fn random_edges(n: usize) -> (usize, usize) {
    let mut a: usize = 0;
    let mut c: usize = 0;
    while a.abs_diff(c) <= 1 || (a == 0 && c == n-1) || (c == 0 && a == n-1) {
        a = thread_rng().gen_range(0..n);
        c = thread_rng().gen_range(0..n);
    }
    (a, c)
}

fn swap_edges(cycle: &mut [usize], (a, c): &(usize, usize)) {
    let (a, c) = if c > a {(a, c)} else {(c, a)};
    for delta in 0..(c-a)/2 {
        cycle.swap(a+1+delta, c-delta);
    }
}
