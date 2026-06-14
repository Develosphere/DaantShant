"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import styles from "./landing.module.css";

const NAV = [
  { href: "#home", label: "Home" },
  { href: "#how-it-works", label: "How It Works" },
  { href: "#features", label: "Features" },
  { href: "#why", label: "About" },
  { href: "#team", label: "FAQ" },
];

const FEATURES = [
  {
    title: "AI Dental Scanner",
    desc: "Upload a photo and receive instant insights.",
  },
  {
    title: "Smart Dental Assistant",
    desc: "Ask questions about oral health anytime.",
  },
  {
    title: "Nearby Dentists",
    desc: "Get recommendations based on your location.",
  },
  {
    title: "Smart Reminders",
    desc: "Never forget brushing, flossing, or checkups.",
  },
  {
    title: "Personalized Tips",
    desc: "Receive recommendations tailored to your habits.",
  },
];

const STEPS = [
  { title: "Scan", desc: "Upload or capture a photo of your teeth." },
  { title: "Analyze", desc: "AI detects visible signs and issues." },
  { title: "Report", desc: "Get a clear diagnosis summary instantly." },
  { title: "Chat", desc: "Ask your AI dental assistant follow-ups." },
  { title: "Connect", desc: "Find trusted dentists when you need care." },
];

const WHY = [
  {
    heading: "Detect Earlier",
    color: "blue" as const,
    text: "Identify visible signs before they become severe.",
    emoji: "🔍",
  },
  {
    heading: "Save Money",
    color: "blue" as const,
    text: "Early detection costs less than major treatments.",
    emoji: "💰",
    reverse: true,
  },
  {
    heading: "Better Habits",
    color: "blue" as const,
    text: "Build daily routines that protect your smile.",
    emoji: "✨",
  },
  {
    heading: "Find Dentists Faster",
    color: "navy" as const,
    text: "Trusted recommendations when you need help.",
    emoji: "⚕️",
    reverse: true,
  },
];

const TEAM = [
  { name: "Laraib", img: "/landing/team-laraib.png" },
  { name: "Hasnain", img: "/landing/team-hasnain.png" },
  { name: "Anas", img: "/landing/team-anas.png" },
  { name: "Nathan", img: "/landing/team-nathan.png" },
];

export function LandingPage() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className={styles.page}>
      <header className={styles.nav}>
        <div className={styles.navInner}>
          <Link href="/" className={styles.logo}>
            <Image
              src="/landing/logo.png"
              alt="DantShaant"
              width={120}
              height={48}
              className={styles.logoImg}
              priority
            />
          </Link>

          <nav
            className={`${styles.navLinks} ${menuOpen ? styles.navLinksOpen : ""}`}
            aria-label="Main"
          >
            {NAV.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className={styles.navLink}
                onClick={() => setMenuOpen(false)}
              >
                {item.label}
              </a>
            ))}
            <Link href="/patient/register" className={styles.navCta}>
              Get Started
            </Link>
          </nav>

          <button
            type="button"
            className={styles.menuBtn}
            aria-label="Toggle menu"
            onClick={() => setMenuOpen((o) => !o)}
          >
            ☰
          </button>
        </div>
      </header>

      <section id="home" className={styles.hero}>
        <div className={styles.heroBg} aria-hidden />
        <div className={`${styles.heroOrb} ${styles.heroOrbA}`} aria-hidden />
        <div className={`${styles.heroOrb} ${styles.heroOrbB}`} aria-hidden />

        <div className={styles.heroCopy}>
          <h1 className={styles.heroScan}>Scan</h1>
          <p className={styles.heroDetect}>Detect.</p>
          <p className={styles.heroProtect}>Protect.</p>
          <p className={styles.heroStat}>
            95% of people ignore dental issues until it&apos;s too late.
          </p>
          <Link href="/scan" className={styles.scanCta}>
            <Image
              src="/landing/tooth-icon.png"
              alt=""
              width={28}
              height={28}
              className={styles.scanCtaIcon}
            />
            Scan My Teeth
          </Link>
        </div>

        <div className={styles.heroVisual}>
          <Image
            src="/landing/hero-mascot.png"
            alt="DantShaant tooth mascot"
            width={557}
            height={416}
            className={styles.heroMascot}
            priority
          />
        </div>
      </section>

      <section id="features" className={styles.features}>
        <div className={styles.featuresInner}>
          <h2 className={styles.sectionLabel}>FEATURES SECTION</h2>
          <p className={styles.sectionSub}>
            Everything You Need For Better Oral Health
          </p>
          <div className={styles.featureGrid}>
            {FEATURES.map((f) => (
              <article key={f.title} className={styles.featureCard}>
                <h3 className={styles.featureTitle}>{f.title}</h3>
                <p className={styles.featureDesc}>{f.desc}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="how-it-works" className={styles.blueprint}>
        <div className={styles.blueprintInner}>
          <h2 className={styles.blueprintTitle}>How It Works</h2>
          <Image
            src="/landing/steps-blueprint.png"
            alt="5-step DantShaant blueprint process"
            width={1232}
            height={413}
            className={styles.blueprintImg}
          />
          <div className={styles.stepsFallback} aria-label="5-step process">
            {STEPS.map((step, i) => (
              <article key={step.title} className={styles.stepCard}>
                <span className={styles.stepNum}>{i + 1}</span>
                <h3 className={styles.stepTitle}>{step.title}</h3>
                <p className={styles.stepDesc}>{step.desc}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="why" className={styles.why}>
        <h2 className={styles.whyTitle}>Why DantShaant?</h2>
        <div className={styles.whyGrid}>
          {WHY.map((item) => (
            <div
              key={item.heading}
              className={`${styles.whyRow} ${item.reverse ? styles.whyRowReverse : ""}`}
            >
              <div>
                <h3
                  className={`${styles.whyHeading} ${
                    item.color === "navy" ? styles.whyHeadingNavy : styles.whyHeadingBlue
                  }`}
                >
                  {item.heading}
                </h3>
                <p className={styles.whyText}>{item.text}</p>
              </div>
              <div className={styles.whyVisual}>
                <div className={styles.whyBlob}>{item.emoji}</div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section id="team" className={styles.team}>
        <div className={styles.teamInner}>
          <h2 className={styles.teamTitle}>Smile With Confidence</h2>
          <p className={styles.teamSub}>Healthy teeth. Better confidence.</p>
          <div className={styles.teamGrid}>
            {TEAM.map((member) => (
              <figure key={member.name} className={styles.teamCard}>
                <Image
                  src={member.img}
                  alt={member.name}
                  width={400}
                  height={500}
                />
                <figcaption className={styles.teamName}>{member.name}</figcaption>
              </figure>
            ))}
          </div>
        </div>
      </section>

      <footer className={styles.footer}>
        <div className={styles.footerInner}>
          <div>
            <p className={styles.footerBrand}>DantShaant</p>
            <p>Autonomous dental AI — scan, chat, and connect with care.</p>
          </div>
          <div className={styles.footerCol}>
            <h4>Useful Links</h4>
            <Link href="/scan">AI Scanner</Link>
            <Link href="/chat">AI Chat</Link>
            <Link href="/patient/login">Patient Portal</Link>
            <Link href="/dentist/login">Dentist Portal</Link>
          </div>
          <div className={styles.footerCol}>
            <h4>Explore More</h4>
            <Link href="/portal">Products</Link>
            <Link href="/patient/register">Get Started</Link>
            <Link href="#how-it-works">How It Works</Link>
          </div>
        </div>
        <p className={styles.footerBottom}>DantShaant © 2026 · All rights reserved</p>
      </footer>
    </div>
  );
}
