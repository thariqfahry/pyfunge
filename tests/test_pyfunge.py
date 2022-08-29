import io
import sys

from pyfunge.interpreter import Interpreter

def test_quine(capsys):
    quine = "01->1# +# :# 0# g# ,# :# 5# 8# *# 4# +# -# _@"
    Interpreter(quine).run()
    assert capsys.readouterr().out == quine

def test_quine2(capsys):
    quine = '"48*2+,>:#,_@                                                       @_,#:>,+2*84'
    Interpreter(quine).run()
    assert capsys.readouterr().out == quine    

def test_semiquine(capsys):
    Interpreter('<@,+2*48_,#! #:<,_$#-:#*8#4<8"').run()
    assert capsys.readouterr().out == '@,+2*48_,#! #:<,_$#-:#*8#4<8"'

def test_multi(capsys):
    program = \
    """
1-0g:"Z"-#v_$91+"sparw tup/teG">:#,_$               v                          Z
          >:" "-#v_$91+"ecaps snruter teg BOO">:#,_$v
v                >0" snruter teg BOO">:#,_$.91+,    >
>8:+:*11p11g#v_91+"tib 8 dengis"01-11p11g!#v_"nu">" era slleC">:#,_v
vv           >91+"tib 8>"                  >     ^                 >91+"krow " #
 >        >"spmuj egdE">:#,_   91+"krow "04-3%1+#v_        >"sredniamer evitag"v
>"ton od "^                                      >"ton od "^
"eN">:#,_  91+"skrow edomgnirts ni @">:#,_@                                    >
    """

    output = \
    """Get/put wraps
Cells are >8 bit
Edge jumps work
Negative remainders work
@ in stringmode works
"""

    with open("./tests/test_multi.bf") as f:
        Interpreter(f.read()).run()
    assert capsys.readouterr().out == output


