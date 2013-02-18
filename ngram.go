package main

import (
	"fmt"
	"strings"
	)

var ngram_db = make(map[string]int)

func build_db(txt string){
	txt = strings.TrimSpace(txt)
	if _,ok := ngram_db[txt]; ok {
		ngram_db[txt]++
	} else {
		ngram_db[txt] = 1
	}
}

func ngram(txt string, n int){
	words := strings.Split(txt, " ")

	i := 0
	limit := len(words) - (n - 1)
	for i < limit {
		build_db(strings.Join(words[i:(i+n)], " "))
		i++;
	}
}

func main(){
	txt := "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus eget nunc id turpis porttitor pellentesque. Morbi nec leo in augue accumsan dignissim. Suspendisse potenti. Donec at ligula augue, quis fermentum enim. Integer feugiat sollicitudin posuere. Etiam convallis tincidunt leo in sollicitudin. Mauris fermentum nibh a diam tempor feugiat. Integer malesuada varius mattis. Praesent et urna ut orci lacinia tempus vel pharetra felis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus eget nunc id turpis porttitor pellentesque. Morbi nec leo in augue accumsan dignissim. Suspendisse potenti. Donec at ligula augue, quis fermentum enim. Integer feugiat sollicitudin posuere. Etiam convallis tincidunt leo in sollicitudin. Mauris fermentum nibh a diam tempor feugiat. Integer malesuada varius mattis. Praesent et urna ut orci lacinia tempus vel pharetra felis. "
	
	sentences := strings.Split(txt, ".")
	for _, sentence := range sentences {
		ngram(strings.TrimSpace(sentence), 3)
	}
	fmt.Println(ngram_db)
}