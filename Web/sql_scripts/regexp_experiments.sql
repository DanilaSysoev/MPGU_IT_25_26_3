-- SELECT 'abc' ~ '^abc$';
-- SELECT 'xabcy' ~ '^abc$';
-- SELECT 'xabcy' ~ 'abc';
-- SELECT 'xabcy' ~ 'a.c';
-- SELECT 'xazcy' ~ 'a.c';
-- SELECT 'xazzzcy' ~ 'a*c';
-- SELECT 'xaz34cy' ~ 'a[[:digit:]]+c';
-- SELECT 'xa123cy' ~ 'a[[:digit:]]+c';
-- SELECT 'xacy' ~ 'a[[:digit:]]+c';
-- SELECT 'xa123cy' ~ 'A[[:digit:]]+c';
-- SELECT 'xa123cy' ~* 'A[[:digit:]]+c';

-- ~ - совпадает
-- !~ - не совпадает
-- ~* - совпадает без учета регистра
-- !~* - не совпадает без учета регистра

-- SELECT regexp_replace('Hello, world!', 'o', 'O', 'g');
-- SELECT regexp_replace('Hello, world!', '[[:punct:]]', '', 'g');
-- SELECT regexp_replace('Hello, world!', 'o', 'O', 'g');

-- SELECT unnest(regexp_match('sysoevdu@sample.net', '(.*)@(.*)'));

-- SELECT regexp_replace('<h1>Text</h1>\n<h1>Text 2</h1>', '<h1>([^<>]*)</h1>', '# \1', 'g');

-- SELECT regexp_match('sysoevdu@sample.net ivanI@sample.net, ', '([^[:space:]]*)@([^[:space:]]*)');
-- SELECT unnest(regexp_matches('sysoevdu@sample.net ivanI@sample.net', '([^[:space:]]*)@([^[:space:]]*)', 'g'));

SELECT regexp_split_to_array('Hello, world! My name is Danila.', '[[:space:][:punct:]]+');
SELECT regexp_split_to_table('Hello, world! My name is Danila.', '[[:space:][:punct:]]+');