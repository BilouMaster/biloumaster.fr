months = {
    '01':'janvier',
    '02':'février',
    '03':'mars',
    '04':'avril',
    '05':'mai',
    '06':'juin',
    '07':'juillet',
    '08':'août',
    '09':'septembre',
    '10':'octobre',
    '11':'novembre',
    '12':'décembre'
}

def str_date_fr(date: str) -> str:
    date = date.split('-')
    if len(date) == 3 and date[2][0] == '0':
        date[2] = date[2][1]
        if date[2] == '1':
            date[2] += '<sup>er</sup>'
    if len(date) == 1:
        return date[0]
    else:
        date[1] = months[date[1]]
        return ' '.join(reversed(date))