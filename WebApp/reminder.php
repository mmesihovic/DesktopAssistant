<?php
    class Reminder {
        public $year;
        public $month;
        public $day;
        public $hour;
        public $minute;
        public $reminder;
        
        function __construct($y,$mo,$da,$ho,$min, $r) {
            if($y >2010 && $y<2100 && $mo >0 && $mo<13 && $da >0 && $da<32 && $ho >=0 && $ho<25 && $min >=0 && $min<61) {   /*
                $this->year = $y;
                $this->month = $mo;
                $this->day = $da;
                $this->hour = $ho;
                $this->minute = $min; 
                $this->reminder = $r;
                */
                $this->year = $y . '';
                if(strlen($mo.'')==1) {
                    $this->month = '0'.$mo;
                }
                else {
                    $this->month = $mo . '';
                }
                if(strlen($da.'')==1) {
                    $this->day = '0'.$da;
                }
                else {
                    $this->day = $da . '';
                }
                if(strlen($ho.'')==1) {
                    $this->hour = '0'.$ho;
                }
                else {
                    $this->hour = $ho . '';
                }
                if(strlen($min.'')==1) {
                    $this->minute = '0'.$min;
                }
                else {
                    $this->minute = $min . '';
                }
                $this->reminder = $r;
            }
        }
        function toArray() {
            return array($this->year,$this->month,$this->day,$this->hour,$this->minute,$this->reminder);
        }
        function printDate() {
            echo ($this->day . ".".$this->month.".".$this->year." at ".$this->hour.":".$this->minute);
        }
        
    }

    function cmp($a, $b) {
        if($a->year < $b->year) return false;
        else if($a->year == $b->year) {
            if($a->month < $b->month) return false;
            else if($a->month == $b->month) {
                if($a->day < $b->day) return false;
                else if($a->day == $b->day) {
                    if($a->hour < $b->hour) return false;
                    else if($a->hour == $b->hour) {
                        if($a->minute < $b->minute) return false;
			else return true;
                    }
		    else return true;
                }
                else return true;  
            }
	    else return true;
        }
        else return true;
    }
?>