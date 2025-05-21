"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { useAuth } from "@/hooks/use-auth"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Menu, X, User } from "lucide-react"

export default function Header() {
  const { user, signOut } = useAuth()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-2">
          <span className="font-bold text-xl text-green-600">BioForge</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-6">
          <Link href="/designer" className="text-gray-600 hover:text-green-600">
            Designer
          </Link>
          <Link href="/explore" className="text-gray-600 hover:text-green-600">
            Explore
          </Link>
          <Link href="/learn" className="text-gray-600 hover:text-green-600">
            Learn
          </Link>
          <Link href="/community" className="text-gray-600 hover:text-green-600">
            Community
          </Link>
        </nav>

        {/* Auth Buttons */}
        <div className="hidden md:flex items-center space-x-4">
          {user ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <User className="h-5 w-5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuLabel>My Account</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild>
                  <Link href="/profile">Profile</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/my-designs">My Designs</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/settings">Settings</Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => signOut()}>Log out</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <>
              <Button asChild variant="ghost">
                <Link href="/login">Log in</Link>
              </Button>
              <Button asChild className="bg-green-600 hover:bg-green-700">
                <Link href="/signup">Sign up</Link>
              </Button>
            </>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button className="md:hidden" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
          {mobileMenuOpen ? <X className="h-6 w-6 text-gray-600" /> : <Menu className="h-6 w-6 text-gray-600" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden px-4 py-4 bg-white border-t border-gray-200">
          <nav className="flex flex-col space-y-4">
            <Link
              href="/designer"
              className="text-gray-600 hover:text-green-600"
              onClick={() => setMobileMenuOpen(false)}
            >
              Designer
            </Link>
            <Link
              href="/explore"
              className="text-gray-600 hover:text-green-600"
              onClick={() => setMobileMenuOpen(false)}
            >
              Explore
            </Link>
            <Link href="/learn" className="text-gray-600 hover:text-green-600" onClick={() => setMobileMenuOpen(false)}>
              Learn
            </Link>
            <Link
              href="/community"
              className="text-gray-600 hover:text-green-600"
              onClick={() => setMobileMenuOpen(false)}
            >
              Community
            </Link>

            {user ? (
              <>
                <Link
                  href="/profile"
                  className="text-gray-600 hover:text-green-600"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Profile
                </Link>
                <Link
                  href="/my-designs"
                  className="text-gray-600 hover:text-green-600"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  My Designs
                </Link>
                <button
                  onClick={() => {
                    signOut()
                    setMobileMenuOpen(false)
                  }}
                  className="text-left text-gray-600 hover:text-green-600"
                >
                  Log out
                </button>
              </>
            ) : (
              <div className="flex flex-col space-y-2 pt-2">
                <Button asChild variant="outline">
                  <Link href="/login" onClick={() => setMobileMenuOpen(false)}>
                    Log in
                  </Link>
                </Button>
                <Button asChild className="bg-green-600 hover:bg-green-700">
                  <Link href="/signup" onClick={() => setMobileMenuOpen(false)}>
                    Sign up
                  </Link>
                </Button>
              </div>
            )}
          </nav>
        </div>
      )}
    </header>
  )
}
