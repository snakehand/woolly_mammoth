use num::integer::gcd;

const NUM: usize = 1000000;

#[derive(Debug)]
struct Number {
    num: u32,
    next: u32,
}

// Returns True if n has more than 1 prime factor
fn check_factors(n: u32) -> bool {
    let mut f1 = 0;
    for i in 2.. {
        if n % i == 0 {
            f1 = i;
            break;
        }
        if i * i > n {
            return false;
        }
    }
    let mut n2 = n / f1;
    while n2 % f1 == 0 {
        n2 /= f1;
    }
    n2 != 1
}

fn main() {
    // Build a linked list of all composit numbers ..NUM
    let mut taken: Vec<Number> = Vec::with_capacity(NUM);
    let mut next = 1;
    for i in 1..(NUM as u32) {
        if check_factors(i) {
            let tk = Number {
                num: i as u32,
                next,
            };
            taken.push(tk);
            next += 1;
        }
    }
    let last_idx = taken.len() - 1;
    taken[last_idx].next = 0;

    // println!("{} {:?}", taken.len(), &taken[0..10]);

    // Search for next number in sequence
    let mut prev2 = 2;
    let mut prev = 6;
    'outer: loop {
        // println!("NEXT: {} {}", prev2, prev);
        let mut n_idx = 0;
        'inner: loop {
            if taken[n_idx].next == 0 {
                break; // End of list / search
            }
            // Advance 1 element in remaining list
            let last_n = n_idx;
            n_idx = taken[n_idx].next as usize;
            let num = taken[n_idx].num;
            // println!("-> {} {} {}", num, gcd(num,prev), gcd(num,prev2));

            // Test GCD with 2 previous elements
            let mut g = gcd(num, prev);
            if g != 1 && gcd(num, prev2) == 1 {
                // Test for "dead end" by ensuring that n has
                // at least 1 distinct factor from previous number
                let mut fb = num / g;
                loop {
                    // println!("   {} {} {}", prev, fb, g);
                    if g == 1 {
                        if fb > 1 {
                            // Remainder found after removing common factors
                            break;
                        } else {
                            // Remainder is 1 - try next number
                            // println!("skip {}", num);
                            continue 'inner;
                        }
                    }
                    g = gcd(fb, prev);
                    fb = fb / g;
                }
                // Next number in sequence found, unlink it from the list
                prev2 = prev;
                prev = num;
                taken[last_n].next = taken[n_idx].next;
                println!("{}", num);
                continue 'outer;
            }
        }
        break;
    }
}
