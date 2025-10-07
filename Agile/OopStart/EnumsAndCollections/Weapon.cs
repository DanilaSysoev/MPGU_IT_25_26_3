namespace EnumsAndCollections;

public class Weapon
{
    public Damage Damage { get; init; }

    public Weapon(Damage damage)
    {
        Damage = damage;
    }
}
