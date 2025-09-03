using DataStructures;

namespace DataStructuresTests;

public class Tests
{
    private DynamicArray<int> dynamicArray;
    private DynamicArray<int> emptyArray;

    [SetUp]
    public void Setup()
    {
        dynamicArray = new DynamicArray<int>();
        dynamicArray.PushBack(10);
        dynamicArray.PushBack(20);
        dynamicArray.PushBack(30);
        dynamicArray.PushBack(40);
        dynamicArray.PushBack(50);

        emptyArray = new DynamicArray<int>();
    }

    [Test]
    public void Size_NewArrayCreated_EqualsZero()
    {
        Assert.That(emptyArray.Size, Is.EqualTo(0));
    }
}