namespace GameEngine;

public interface IAttackable
{
    int Hp { get; }

    void TakeDamage(int damage);
}
