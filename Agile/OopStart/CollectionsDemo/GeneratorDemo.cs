using System.Collections;

namespace CollectionsDemo;

public class GeneratorDemo : IEnumerable<int>
{
    public IEnumerator<int> GetEnumerator()
    {
        Random random = new Random(100);

        int number = random.Next(100);
        while (number != 0)
        {
            yield return number;
            number = random.Next(100);
        }
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }
}
