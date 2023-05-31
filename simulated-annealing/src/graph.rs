#[derive(Debug)]
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
}
