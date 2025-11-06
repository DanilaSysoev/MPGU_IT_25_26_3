import argparse
import json
import auth
import user

def cmd_login(a):
    try:
        access, refresh = auth.login(a.username, a.password)
        print(json.dumps({"access_token": access, "refresh_token": refresh}))
        return 0
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1

def cmd_me(a):
    try:
        payload = auth.verify_access(a.access)
        print(json.dumps(payload, ensure_ascii=False))
        return 0
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1

def cmd_refresh(a):
    try:
        access, refresh = auth.refresh_pair(a.refresh)
        print(json.dumps({"access_token": access, "refresh_token": refresh}))
        return 0
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1

def cmd_revoke(a):
    try:
        auth.revoke(a.token)
        print("OK")
        return 0
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1

def cmd_introspect(a):
    res = auth.introspect(a.token)
    print(json.dumps(res, ensure_ascii=False))
    return 0 if res.get("active") else 1

def cmd_users_add(a):
    try:
        user.register_user(a.username, a.email, a.password)
        print("OK")
        return 0
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1

def build():
    p = argparse.ArgumentParser(description="auth-cli")
    sub = p.add_subparsers(dest="cmd", required=True)

    lg = sub.add_parser("login")
    lg.add_argument("--username", required=True)
    lg.add_argument("--password", required=True)
    lg.set_defaults(func=cmd_login)

    me = sub.add_parser("me")
    me.add_argument("--access", required=True)
    me.set_defaults(func=cmd_me)

    rf = sub.add_parser("refresh")
    rf.add_argument("--refresh", required=True)
    rf.set_defaults(func=cmd_refresh)

    rv = sub.add_parser("revoke")
    rv.add_argument("--token", required=True)
    rv.set_defaults(func=cmd_revoke)

    it = sub.add_parser("introspect")
    it.add_argument("--token", required=True)
    it.set_defaults(func=cmd_introspect)

    ua = sub.add_parser("users")
    ua_sub = ua.add_subparsers(dest="ucmd", required=True)
    add = ua_sub.add_parser("add")
    add.add_argument("--username", required=True)
    add.add_argument("--email", required=True)
    add.add_argument("--password", required=True)
    add.set_defaults(func=cmd_users_add)

    return p

def main():
    parser = build()
    args = parser.parse_args()
    raise SystemExit(args.func(args))

if __name__ == "__main__":
    main()
