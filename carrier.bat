@echo '!!!Не работает количестово: в строке Tritium 515 720 52 494 710M 0.43 читает 710М как количество, а не как время!!!'
trade.py run --capacity 1000 --credits 1b --from %1 --direct --ly-per 500 --pad-size L --no-planet -vv
trade.py market %1 --selling -vv