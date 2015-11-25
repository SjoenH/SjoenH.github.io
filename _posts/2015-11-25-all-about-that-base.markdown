---
layout: post
title:  "All about that base"
date:   2015-11-25 11:23:19 +0100
categories: digdat number binary decimal hex
---
Base 10 er det tallsystemet som vi ellers bruker til å regne med. De fleste datamaskiner bruker bare to tilstander: '0' og '1' til å representere all data.

*Oktale tall er nyttige fordi de kan brukes til å representere grupper på 3 binære siffer (3 binære siffer kan benyttes til å telle fra 0 til 7). Hexadesimale tall er tilsvarende nyttige fordi de kan brukes til å representere grupper på 4 binære siffer.*

Base 2|Base 10|Base 16
------|-------|-------
100   |   4   |4
1111  |  15   |F

Decimal|0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|
---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---
Binary	|0|1|10|11|100|101|110|111|1000|1001|1010|1011|1100|1101|1110|1111|
Hex		|0|1|2|3|4|5|6|7|8|9|A|B|C|D|E|F|

##Base 2 / Binary
La oss ta for oss ett 8-bit system...

Base 2 | Base 10
---|---
0000 0000 | 0
0000 0001 | 1
0000 0010 | 2
... | ...
0000 1000 | 8
1000 0000 | 128
1111 1111 | 255


##Negative numbers in binary (base 2)
*"The early days of digital computing were marked by a lot of competing ideas about both hardware technology and mathematics technology (numbering systems). One of the great debates was the format of negative numbers, with some of the era's most expert people having very strong and different opinions.*

*One camp supported **two's complement**, the system that is dominant today. Another camp supported **ones' complement**, where any positive value is made into its negative equivalent by inverting all of the bits in a word. A third group supported **"sign & magnitude"** (sign-magnitude), where a value is changed from positive to negative simply by toggling the word's sign (high-order) bit."* - [Wikipedia](https://en.wikipedia.org/wiki/Signed_number_representations)

###Signed Number
-
Ved bruk av sign-magnitude reserveres det mest signifikante bitet (dvs det sifferet som står lengst til venstre) til å angi fortegn. Resten angir tallets absoluttverdi. Dersom fortegsbitet er satt er tallet negativt.

Ulempen med dette er at vi får to måter å skrive 0 på; -0 og +0.

To represent a negative number in binary with signed notation just add a 1 in front of the positive number.

Decimal|-4  |-3  |  -2|  -1|  -0|   0|   1|   2|   3|   4|
    ---|--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |
Binary |1100|1011|1010|1001|1000|0000|0001|0010|0011|0100|

*Same data under as over*

Decimal|-4  |-3  |  -2|  -1|  -0|
---|---|--- |--- |--- |--- |--- |
Binary |1100|1011|1010|1001|1000|

Decimal|4  |3    |   2|   1|   0|
---|---|--- |--- |--- |--- |--- |
Binary |0100|0011|0010|0001|0000|

---
####The *Good*
Easy to remember.
####The *Bad*
Hard to calculate with.

---

###Ones complement
-
Another way to represent negative values in binary is:

	Take a positive binary number
	and invert the digits.

Example:

	   0110
	-> 1001



---
####The *Good*
Now you can add a negative number to another number!
####The *Bad*

---

###Two's complement
-

Den måten som i (nesten) alle tilfeller benyttes i dag er toerskomplement. Har du et binært tall på toerskomplement form kan du finne det negative tallet med samme absoluttverdi ved å invertere alle bitene og legge til én. Samme fremgangsmåte for å finne det positive tallet hvis du har et negativt binært tall. Den generelle formelen ser slik ut:

	−X = ¬X + 1

Denne metoden har flere fordeler. Vi har fremdeles egenskapen at mest signifikante bit sier hvilket fortegn tallet har. Toerskomplements form har også mange fordeler med hensyn på aritmetikk.

The Third way to represent negative values in binary is:

	Take a positive binary number, invert the digits  (*Bitwise not*) and add 1.

Example:

	Lets take the decimal number 6
	and use the Two's complement notation for negative numbers.

	   0110
	-> 1001
	+ 1
	=  1010

	That is -6 in base 10


---
####The *Good*
####The *Bad*

---

#Base 16 / Hexadecimal
We often write "0x" in front of the number just so that we know we are using *base 16*, aka Hexadecimal notation.

Decimal|0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|
---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---
Hex|0|1|2|3|4|5|6|7|8|9|A|B|C|D|E|F|


Often used in declaring color in for example html code.


#IEEE 32
See: [http://www.h-schmidt.net/FloatConverter/IEEE754.html](http://www.h-schmidt.net/FloatConverter/IEEE754.html)
