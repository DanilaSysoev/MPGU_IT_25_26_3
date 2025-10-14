using System.Text;

namespace Delegates;

public delegate void ProcessDelegate(StringBuilder text);

public class TextProcessor
{
    public ProcessDelegate? Processor { get; set; }

    public TextProcessor(ProcessDelegate processor)
    {
        Processor = processor;
    }

    public string Process(string text)
    {
        var sb = new StringBuilder(text);
        Processor!(sb);
        return sb.ToString();
    }
}
