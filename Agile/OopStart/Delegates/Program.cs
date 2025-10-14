using System.Text;
using Delegates;

static int EvenFirst(int lo, int ro)
{
    if (lo % 2 != 0 && ro % 2 == 0)
        return 1;
    if (lo % 2 == 0 && ro % 2 != 0)
        return -1;
    return 0;
}

static void ReplaceSpaces(StringBuilder text)
{
    text.Replace(" ", "_");
}
static void ToUpper(StringBuilder text)
{
    for (int i = 0; i < text.Length; i++)
        text[i] = char.ToUpper(text[i]);
}

var data = new int[] { 6, 2, 9, 0, 7, 1, 5, 8, 1, 4 };
Sorter sorter = new Sorter(data, EvenFirst);
sorter.Sort();
foreach (var item in sorter.Sorted)
{
    Console.Write("{0} ", item);
}

TextProcessor processor = new TextProcessor(ReplaceSpaces);
processor.Processor += ToUpper;
processor.Processor += (text) =>
{
    text.Replace(".", "")
        .Replace("!", "")
        .Replace("?", "")
        .Replace(",", "");
};

Console.WriteLine(processor.Process("Hello World!"));

processor.Processor -= ToUpper;
Console.WriteLine(processor.Process("Hello World!"));
