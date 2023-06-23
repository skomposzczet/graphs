use std::ops::Index;

#[derive(Debug, Clone)]
pub struct Point {
    pub x: i32,
    pub y: i32,
}

impl Point {
    pub fn from_str(line: &str) -> Point {
        let (xstr, ystr) = line.split_once(" ").unwrap();
        Point {
            x: xstr.parse().unwrap(),
            y: ystr.parse().unwrap(),
        }
    }

    pub fn distance(&self, other: &Point) -> f32 {
        let x2 = (self.x - other.x).pow(2);
        let y2 = (self.y - other.y).pow(2);
        return f32::sqrt((x2 + y2) as f32);
    }
}

pub struct Graph {
    data: Vec<Point>,
}

impl Graph {
    pub fn new(points: Vec<Point>) -> Self {
        Graph{ data: points }
    }

    pub fn len(&self) -> usize {
        self.data.len()
    }
}

impl Index<usize> for Graph {
    type Output = Point;

    fn index(&self, index: usize) -> &Point {
        &self.data[index]
    }
}
