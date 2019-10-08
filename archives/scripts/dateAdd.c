/*___________________________________________________________________________________*
*                                                                                    *
*  Author        :-  Ajit Isack                                                      *
*  Date Created  :-  20120815                                                        *
*  Description   :-  This C program adds/subtracts either years, months or days      *
*                    to/from a supplied date                                         *
*____________________________________________________________________________________*/

#include <stdlib.h>
#include <stdio.h>

char* dateAdd(char* freq, char* inDate, int count);

int main(int argc, char *argv[])
{
        if (argc != 4)
        {
                printf("Usage   : %s <years|months|days> <date in the format YYYYMMDD> <count>\n", argv[0]);
                printf("Example : %s years 20120104 10\n", argv[0]);
                exit (1);
        }
        printf("%s\n", dateAdd(argv[1], argv[2], atoi(argv[3])) );
        return(0);
}

char* dateAdd(char* freq, char* inDate, int count)
{
        int i, j, n, no_of_days;
        int LEAP_YEAR = 0;
        int yy, mm, dd;
        char *newDate = (char *)malloc(sizeof(char) * 8);
        char *error = "********";
        yy = mm = dd = 0;
        int numberOfDays[] = { 0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };


        /*** Check whether the supplied Date is valid or not ***/
        i = -1;
        while( inDate[++i] != 0 && inDate[i] >= '0' && inDate[i] <= '9' );
        if ( i != 8 ) return(error);

        i = 8; j = 1;
        while( --i >= 0 )
        {
                if ( i == 5 || i == 3 ) j = 1;
                if ( i <= 7 && i >= 6 ) dd = dd + ( (inDate[i] - 48 ) * j );
                if ( i <= 5 && i >= 4 ) mm = mm + ( (inDate[i] - 48 ) * j );
                if ( i <= 3 && i >= 0 ) yy = yy + ( (inDate[i] - 48 ) * j );
                j = j * 10;
        }

        if ( mm > 12 || mm < 1 ) return(error);

        if ( dd > 31 || mm < 1 ) return(error);

        if ( dd > 30 && (mm == 4 || mm == 6 || mm == 9 || mm == 11) ) return(error);

        if ( mm == 2 ) {
                     if ( yy % 400 == 0 ) LEAP_YEAR = 1;
                else if ( yy % 100 == 0 ) LEAP_YEAR = 0;
                else if ( yy % 4   == 0 ) LEAP_YEAR = 1;
                                     else LEAP_YEAR = 0;
                if (  LEAP_YEAR && dd > 29 ) return(error);
                if ( !LEAP_YEAR && dd > 28 ) return(error);
        }



        /*** Add or Subtract YEARS to the Date ***/
        if ( *freq == 'y' || *freq == 'Y' ) {
                yy = yy + count;
        }



        /*** Add or Subtract MONTHS to the Date ***/
        if ( *freq == 'm' || *freq == 'M' ) {
                yy = yy + (count / 12);
                mm = mm + (count % 12);
                if ( mm > 12 )
                {
                        mm = mm - 12;
                        yy++;
                }
                if ( mm < 1 )
                {
                        mm = mm + 12;
                        yy--;
                }
                if ( dd == 31 && ( mm == 4 || mm == 6 || mm == 9 || mm == 11 ) ) dd = 30;
        }



        /*** Handling February for LEAP YEAR ***/
        if ( mm == 2 ) {
                     if ( yy % 400 == 0 ) LEAP_YEAR = 1;
                else if ( yy % 100 == 0 ) LEAP_YEAR = 0;
                else if ( yy % 4   == 0 ) LEAP_YEAR = 1;
                else LEAP_YEAR = 0;
                if ( dd > 28 ){
	            if ( LEAP_YEAR ) dd = 29;
	            else dd = 28;
		  }
        }



        /*** Add or Subtract DAYS to the Date ***/
        if ( *freq == 'd' || *freq == 'D' ) {

                no_of_days = count;

                while (no_of_days > 0)
                {
                             if ( yy % 400 == 0 ) LEAP_YEAR = 1;
                        else if ( yy % 100 == 0 ) LEAP_YEAR = 0;
                        else if ( yy % 4   == 0 ) LEAP_YEAR = 1;
                        else LEAP_YEAR = 0;

                        if ( LEAP_YEAR ) numberOfDays[2] = 29;
                                    else numberOfDays[2] = 28;

                        if ( (dd + no_of_days) > numberOfDays[mm] )
                        {
                                no_of_days = no_of_days - ( numberOfDays[mm] - dd );
                                mm++;
                                if ( mm > 12 )
                                {
                                        yy++;
                                        mm = 1;
                                }
                                dd = 0;
                        }
                        else
                        {
                                dd = dd + no_of_days;
                                no_of_days = 0;
                        }
                }// end of while

                if (no_of_days < 0) no_of_days = no_of_days * -1;

                while (no_of_days > 0)
                {
                             if ( yy % 400 == 0 ) LEAP_YEAR = 1;
                        else if ( yy % 100 == 0 ) LEAP_YEAR = 0;
                        else if ( yy % 4   == 0 ) LEAP_YEAR = 1;
                        else LEAP_YEAR = 0;

                        if ( LEAP_YEAR ) numberOfDays[2] = 29;
                                    else numberOfDays[2] = 28;

                        if ( (dd - no_of_days) < 1 )
                        {
                                no_of_days = no_of_days - dd;
                                mm--;
                                if ( mm < 1 )
                                {
                                        yy--;
                                        mm = 12;
                                }
                                dd = numberOfDays[mm];
                        }
                        else
                        {
                                dd = dd - no_of_days;
                                no_of_days = 0;
                        }
                }// end of while
        }

        i = -1;
        while(++i <= 7) newDate[i] = 48; // 48 is the ascii value of digit 0
        newDate[8] = 0;

        i=4;
        while( yy > 0 && i >= 0 )
        {
                n = yy % 10;
                newDate[--i] = n + 48;
                yy = (yy - n) / 10;
        }

        i=6;
        while( mm > 0 )
        {
                n = mm % 10;
                newDate[--i] = n + 48;
                mm = (mm - n) / 10;
        }

        i=8;
        while( dd > 0 )
        {
                n = dd % 10;
                newDate[--i] = n + 48;
                dd = (dd - n) / 10;
        }

        return(newDate);
}

// EOF
//____________________________________________________________________________________//
