namespace GameEngine;

public class Soldier : IAlive, IWarrior, IAttackable
{
    public int Hunger { get; private set; }
    public int Thirst { get; private set; }
    public int Fatigue { get; private set; }

    public int Hp { get; private set; }
    public int Damage { get; init; }

    public Soldier(int hp, int damage)
    {
        Hp = hp;
        Damage = damage;
        Hunger = 0;
        Thirst = 0;
        Fatigue = 0;
    }

    public void Attack(IAttackable enemy)
    {
        enemy.TakeDamage(Damage);
    }
    public void TakeDamage(int damage)
    {
        if (Hp > 0)
            Hp -= damage;
    }


    public const int MaxHunger = 100;
    public const int MaxThirst = 100;
    public const int MaxFatigue = 100;
}
