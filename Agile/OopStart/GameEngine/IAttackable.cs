namespace GameEngine;

public interface IAttackable
{
    int Hp { get; set; }

    void TakeDamage(int damage)
    {
        Hp -= damage;
    }
}
