# coding: utf8

from __future__ import division, print_function, unicode_literals

# value, result, formatcode
examples = (
    (1234.59, '1234.6', '####.#'),
    (8.9, '8.900', '#.000'),
    (0.631, '0.6', '0.#'),
    (12, '12.0', '#.0#'),
    (1234.568, '1234.57', '#.0#'),
    (44.398, ' 44.398', '???.???'),
    (102.65, '102.65 ', '???.???'),
    (2.8, '  2.8  ', '???.???'),
    (5.25, '5 1/4', '#" "???/???'),
    (5.3, '5 3/10', '#\\ ???/???'),
    (12000, '12,000', '#,###'),
    (12000, '12', '#,'),
    (12200000, '12.2', '0.0'),
    (12, '00012', '00000'),
    (123, '00123', '00000'),
    (12, '00012', '"000"#'),
    (123, '000123', '"000"#'),
    (123, '0123', '"0"#'),
    (1230, '03', 'yy'),  # 14.05.1903
    (1230, '1903', 'yyyy'),
    (1230, '5', 'm'),
    (1230, '05', 'mm'),
    (1230, 'May', 'mmm'),
    (1230, 'May', 'mmmm'),
    (1230, 'M', 'mmmmm'),
    (1230, '14', 'd'),
    (1230, '14', 'dd'),
    (1230, 'Thu', 'ddd'),
    (1230, 'Thursday', 'dddd'),
    (43256.584039351852, '14', 'h'),  # 05.06.2018  14:01:01
    (43256.584039351852, '14', 'hh'),
    (43256.584039351852, '14:1', 'h:m'),
    (43256.584039351852, '1401', 'hmm'),
    (43256.584039351852, '1', 's'),
    (43256.584039351852, '01', 'ss'),
    (43256.584039351852, '2 PM', 'h AM/PM'),
    (43256.584039351852, '2:01 PM', 'h:mm AM/PM'),
    (43256.584039351852, '2:01:01 PM', 'h:mm:ss A/P'),
    (43256.584039351852, '2:01:01.00 PM', 'h:mm:ss.00 A/P'),
    (1, '24:00', '[h]:mm'),
    (1, '1440:00', '[mm]:ss'),
    (1, '86400.00', '[ss].00'),
)
