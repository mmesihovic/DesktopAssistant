# Elektrotehnicki fakultet Univerziteta u Sarajevu
# Godina : 2017
# Predmet : Ugradbeni sistemi
# Profesor : Konjicija Samim
# Asistentica: Zubaca Jasmina
# Studenti:
#       -Mustajbasic Belmin (16796)
#       -Mesihovic Mirza    (17345)
# Kod:


class Reminder:
        Year = 2017
        Month = 1
        Day = 1
        Hour = 0
        Minute = 0
        Text = "Simple Reminder"

        def getDate(self):
                return str(self.Day)+"."+str(self.Month)+"."+str(self.Year)+" "+str(self.Hour)+":"+str(self.Minute)

        def __init__(self,y,m,d,h,min,t):
                self.Year = y
                self.Month = m
                self.Day = d
                self.Hour = h
                self.Minute = min
                self.Text = t

        def getMessage(self):
                return self.Text

