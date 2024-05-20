++ [>+++<-]     c0 = 0 c1 = 6
>
[
  [>]           move right until a zero byte is hit
  ,             read in the byte
  [<]           move left until zero byte is hit
  >-            decrement c1
]
>               move right to c2 where the bytes begin
[.>]            output the stored bytes until a zero byte is hit

++++ [>+++<-] > + .   carriage return
