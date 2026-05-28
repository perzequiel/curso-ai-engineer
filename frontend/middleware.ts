import { NextRequest, NextResponse } from "next/server"

// Gate cosmetico: hardcoded login. La cookie la setea el cliente desde /login.
// No es seguridad real; solo evita acceso casual al dashboard.
export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl
  const authed = req.cookies.get("auth")?.value === "1"

  if (pathname.startsWith("/login")) {
    if (authed) return NextResponse.redirect(new URL("/", req.url))
    return NextResponse.next()
  }

  if (!authed) {
    const url = new URL("/login", req.url)
    return NextResponse.redirect(url)
  }

  return NextResponse.next()
}

export const config = {
  // Excluye assets estaticos, favicon e imagenes. El resto pasa por el middleware.
  matcher: ["/((?!_next/static|_next/image|favicon.ico|icon.*|apple-icon.*|.*\\.(?:png|svg|jpg|jpeg|webp)).*)"],
}
