using DataStructures; // Namespace из вашего файла DynamicArray.cs

namespace DataStructuresTests
{
    [TestFixture]
    public class DynamicArrayTests
    {
        [Test]
        public void New_Array_ShouldBeEmpty()
        {
            var a = new DynamicArray<int>();
            Assert.That(a.Size, Is.EqualTo(0));
        }

        [Test]
        public void PushBack_AppendThreeItems_IncreaseSize()
        {
            var a = new DynamicArray<int>();
            a.PushBack(10);
            a.PushBack(20);
            a.PushBack(30);

            Assert.That(a.Size, Is.EqualTo(3));
        }

        [Test]
        public void PushBack_AppendThreeItems_CorrectValues()
        {
            var a = new DynamicArray<int>();
            a.PushBack(10);
            a.PushBack(20);
            a.PushBack(30);

            Assert.That(a[0], Is.EqualTo(10));
            Assert.That(a[1], Is.EqualTo(20));
            Assert.That(a[2], Is.EqualTo(30));
        }

        [Test]
        public void Indexer_SetAndGet_ShouldWorkWithinBounds()
        {
            var a = new DynamicArray<string>();
            a.PushBack("a");
            a.PushBack("b");
            a.PushBack("c");

            a[1] = "B";
            Assert.That(a[0], Is.EqualTo("a"));
            Assert.That(a[1], Is.EqualTo("B"));
            Assert.That(a[2], Is.EqualTo("c"));
        }

        [Test]
        public void Indexer_GetOutOfRange_ShouldThrow()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);

            Assert.Throws<IndexOutOfRangeException>(() => { var _ = a[-1]; });
            Assert.Throws<IndexOutOfRangeException>(() => { var _ = a[1]; }); // == Size
        }

        [Test]
        public void Indexer_SetOutOfRange_ShouldThrow()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);

            Assert.Throws<IndexOutOfRangeException>(() => a[-1] = 42);
            Assert.Throws<IndexOutOfRangeException>(() => a[1] = 42); // == Size
        }

        [Test]
        public void PopBack_RemoveElements_SizeDecreasing()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);
            a.PushBack(2);
            a.PushBack(3);

            a.PopBack();
            Assert.That(a.Size, Is.EqualTo(2));

            a.PopBack();
            a.PopBack();
            Assert.That(a.Size, Is.EqualTo(0));
        }

        [Test]
        public void PopBack_RemoveElements_ValuesCorrect()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);
            a.PushBack(2);
            a.PushBack(3);

            a.PopBack();
            Assert.That(a[0], Is.EqualTo(1));
            Assert.That(a[1], Is.EqualTo(2));

            a.PopBack();
            Assert.That(a[0], Is.EqualTo(1));
        }

        [Test]
        public void PopBack_OnEmpty_ShouldThrow()
        {
            var a = new DynamicArray<int>();
            Assert.Throws<InvalidOperationException>(() => a.PopBack());
        }

        [Test]
        public void Insert_AtBeginning_ShouldShiftRight()
        {
            var a = new DynamicArray<int>();
            a.PushBack(2);
            a.PushBack(3);

            a.Insert(0, 1);

            Assert.That(a.Size, Is.EqualTo(3));
            Assert.That(a[0], Is.EqualTo(1));
            Assert.That(a[1], Is.EqualTo(2));
            Assert.That(a[2], Is.EqualTo(3));
        }

        [Test]
        public void Insert_AtEnd_ShouldBeEquivalentToPushBack()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);
            a.Insert(1, 2);

            Assert.That(a.Size, Is.EqualTo(2));
            Assert.That(a[0], Is.EqualTo(1));
            Assert.That(a[1], Is.EqualTo(2));
        }

        [Test]
        public void Insert_InMiddle_ShouldShiftTail()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);
            a.PushBack(3);
            a.PushBack(4);

            a.Insert(1, 2);

            Assert.That(a.Size, Is.EqualTo(4));
            Assert.That(a[0], Is.EqualTo(1));
            Assert.That(a[1], Is.EqualTo(2));
            Assert.That(a[2], Is.EqualTo(3));
            Assert.That(a[3], Is.EqualTo(4));
        }

        [Test]
        public void Insert_OutOfRange_ShouldThrow()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);

            Assert.Throws<IndexOutOfRangeException>(() => a.Insert(-1, 10));
            Assert.Throws<IndexOutOfRangeException>(() => a.Insert(2, 10)); // > Size
        }

        [Test]
        public void Remove_AtBeginning_ShouldShiftLeft()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);
            a.PushBack(2);
            a.PushBack(3);

            a.Remove(0);

            Assert.That(a.Size, Is.EqualTo(2));
            Assert.That(a[0], Is.EqualTo(2));
            Assert.That(a[1], Is.EqualTo(3));
        }

        [Test]
        public void Remove_InMiddle_ShouldCloseGap()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);
            a.PushBack(2);
            a.PushBack(3);
            a.PushBack(4);

            a.Remove(2);

            Assert.That(a.Size, Is.EqualTo(3));
            Assert.That(a[0], Is.EqualTo(1));
            Assert.That(a[1], Is.EqualTo(2));
            Assert.That(a[2], Is.EqualTo(4));
        }

        [Test]
        public void Remove_AtEnd_ShouldDecreaseSize()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);
            a.PushBack(2);

            a.Remove(1);

            Assert.That(a.Size, Is.EqualTo(1));
            Assert.That(a[0], Is.EqualTo(1));
        }

        [Test]
        public void Remove_OutOfRange_ShouldThrow()
        {
            var a = new DynamicArray<int>();
            a.PushBack(1);

            Assert.Throws<IndexOutOfRangeException>(() => a.Remove(-1));
            Assert.Throws<IndexOutOfRangeException>(() => a.Remove(1)); // == Size
        }

        [Test]
        public void Supports_ReferenceTypes_And_NullValues()
        {
            var a = new DynamicArray<string?>();
            a.PushBack(null);
            a.PushBack("x");

            Assert.That(a.Size, Is.EqualTo(2));
            Assert.That(a[0], Is.Null);
            Assert.That(a[1], Is.EqualTo("x"));
        }

        [Test]
        public void Growth_ShouldPreserve_AllElementsAndOrder()
        {
            var a = new DynamicArray<int>();
            const int n = 1000;

            for (int i = 0; i < n; i++)
                a.PushBack(i);

            Assert.That(a.Size, Is.EqualTo(n));

            Assert.That(a[0], Is.EqualTo(0));
            Assert.That(a[31], Is.EqualTo(31));
            Assert.That(a[32], Is.EqualTo(32));
            Assert.That(a[999], Is.EqualTo(999));
        }

        [Test]
        public void Complex_Sequence_InsertRemove_ShouldStayConsistent()
        {
            var a = new DynamicArray<int>();
            for (int i = 0; i < 10; i++)
                a.PushBack(i);
            
            a.Insert(0, 100);
            a.Insert(6, 200);
            a.Insert(a.Size, 300);

            a.Remove(0);
            a.Remove(5);
            a.Remove(a.Size - 1);

            Assert.That(a.Size, Is.EqualTo(10));
            for (int i = 0; i < 10; i++)
                Assert.That(a[i], Is.EqualTo(i));
        }
    }
}
