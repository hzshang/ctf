#![feature(const_fn)]
#![feature(asm)]
#![feature(const_str_as_bytes)]
const fn db(x: &str, y: usize, z: u8) -> u8{
    return x.as_bytes()[y]-z;
}
const fn xx(x: u8, y: u8) -> u8 {
    return x/xx(x,y);
}

const FLAG: &'static str = include_str!(concat!("./", "flag"));
const ret:u8 = 1/db(FLAG, 0, 123);


fn main()
{
    println!("Hello, world! {}", read_after_raising_any_exceptions());
}

#[inline(never)]
pub fn read_after_raising_any_exceptions() -> u16
{
	unsafe
	{
		let mut control_word: u16;
		asm!
		(
			"fstcw $0"
			:
				// Output constraints.
				"=m"(control_word)
			:
				// Input constraints.
			:
				// Clobbers.
			:
				// Options.
				"volatile"
		);
		control_word
	}
}
