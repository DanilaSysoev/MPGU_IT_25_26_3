// using Abstraction;

// Parent p = new Parent();
// ChildOne c1 = new ChildOne();
// ChildTwo c2 = new ChildTwo();

// p.PrintInfo();
// c1.PrintInfo();
// c2.PrintInfo();

// Printer printer = new Printer();

// printer.Print(p);
// printer.Print(c1);
// printer.Print(c2);

using Abstraction;

var observer = new FigureObserver();
observer.PrintInfo(new Rectangle(10, 20));
observer.PrintInfo(new Circle(5));
