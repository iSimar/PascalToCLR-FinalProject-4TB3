from P0 import compileString

def testPrettyPrint0():
    compileString("""
program p; begin if false then writeln else
if true then write(5) else write(7)
; write(9) end
""", 'T0.s')

def testPrettyPrint1():
    compileString("""
program p; const ccc = 4 div 3;
type I = integer; type A2=array[1..2]of array[3..4] of record f:boolean;
g, h: integer end;
var v, vv, vvv: boolean;
var ww:record a: array[5..6]of record b:  boolean end; c:boolean end;
     procedure pp(var i,j :I;r:boolean); const c = 3 div 3; begin i := c end;
  begin if v then if ww.c then begin v := true end else v:=false;
  if 3 > 4 then while false do if 5 mod 2=1 then writeln else write(7)
  end
""", 'T1.s')
"""pretty-prints:
program p;
  const 
    ccc = 4 div 3;
  type 
    I = integer;
  type 
    A2 = 
      array [1 .. 2] of 
        array [3 .. 4] of 
          record
            f: boolean;
            g, h: integer
          end;
  var 
    v, vv, vvv: boolean;
  var 
    ww: 
      record
        a: 
          array [5 .. 6] of 
            record
              b: boolean
            end;
        c: boolean
      end;
  procedure pp(var i, j: I; r: boolean);
    const 
      c = 3 div 3;
    begin
      i := c
    end
  begin
    if v then
      if ww.c then
          begin
            v := true
          end
      else
        v := false;
    if 3 > 4 then
      while false do
        if 5 mod 2 = 1 then
          writeln
        else
          write(7)
  end
"""

testPrettyPrint1()