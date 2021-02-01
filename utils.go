package main

func check(err error) {
	if err != nil {
		panic(err)
	}
}
func MinOf(vars ...int) int {
	min := vars[0]

	for _, i := range vars {
		if min > i {
			min = i
		}
	}

	return min
}
