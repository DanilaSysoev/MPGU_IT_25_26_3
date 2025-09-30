namespace GameEngine;

public class Peasant : IAlive, IWorker, IAttackable
{
    public int Hunger { get; private set; } = 0;
    public int Thirst { get; private set; } = 0;
    public int Fatigue { get; private set; } = 0;

    public int Coins { get; private set; } = 0;

    public int Hp { get; private set; }

    public Peasant(int hp)
    {
        Hp = hp;
    }

    public void DoWork()
    {
        if (Hunger < MaxHunger &&
            Thirst < MaxThirst &&
            Fatigue < MaxFatigue)
        {
            Coins += 1;
            Hunger += 2;
            Thirst += 2;
            Fatigue += 5;
        }
    }

    public void TakeDamage(int damage)
    {
        if (Hp > 0)
            Hp -= damage;
    }

    public const int MaxHunger = 200;
    public const int MaxThirst = 200;
    public const int MaxFatigue = 200;
}
