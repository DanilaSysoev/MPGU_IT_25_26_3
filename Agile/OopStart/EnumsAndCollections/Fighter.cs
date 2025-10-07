namespace EnumsAndCollections;

public class Fighter
{
    public int Hp { get; internal set; }
    public Weapon Weapon { get; set; }
    public Debuff Debuff { get; internal set; }

    public Fighter(int hp, Weapon weapon)
    {
        Hp = hp;
        Weapon = weapon;
        Debuff = Debuff.None;
    }

    public void TakeDamageFrom(Weapon weapon)
    {
        weapon.Damage.ApplyTo(this);
    }
}
