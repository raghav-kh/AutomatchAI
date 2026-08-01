export default function SectionHeading({
  title,
  subtitle,
  badge,
  align = "left",
  className = "",
}) {
  const alignClass = align === "center" ? "text-center mx-auto" : "text-left";
  return (
    <div className={`mb-8 ${alignClass} ${className}`}>
      {badge && <div className="mb-3">{badge}</div>}
      <h2 className="text-2xl md:text-3xl font-bold font-display tracking-tight text-[var(--color-text-main)]">
        {title}
      </h2>
      {subtitle && (
        <p className="mt-2 text-sm md:text-base text-[var(--color-text-muted)] max-w-2xl leading-relaxed">
          {subtitle}
        </p>
      )}
    </div>
  );
}
