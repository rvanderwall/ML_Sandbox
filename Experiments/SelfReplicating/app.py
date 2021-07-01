#
# This simple program will write a program (without comments)
# that, when executed, creates an identical version of itself.
#

# The basic idea is this:
#    s='print("s={s}\n{s}")'
#    print("s='{s}'\n{s}")
# But the challenge is getting the special characters right


S1='print(f"S1={chr(39)}{S1}{chr(39)}")'
S2='print(S1)'
print(f"S1='{S1}'\nS2='{S2}'")
print(S1)
print(S2)
