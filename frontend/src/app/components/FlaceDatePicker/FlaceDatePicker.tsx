"use client";

import { useState, useRef, useEffect } from "react";
import "./flace-date-picker.css";

interface FlaceDatePickerProps {
  value: string; // "YYYY-MM-DD" or ""
  onChange: (value: string) => void;
  placeholder?: string;
  eventDates?: string[]; // 이벤트 표시용 날짜 목록
}

const WEEKDAYS = ["일", "월", "화", "수", "목", "금", "토"];
const MONTHS = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"];

export default function FlaceDatePicker({
  value,
  onChange,
  placeholder = "날짜 선택",
  eventDates = [],
}: FlaceDatePickerProps) {
  const today = new Date();
  const [open, setOpen] = useState(false);
  const [view, setView] = useState<"calendar" | "year" | "month">("calendar");

  const [viewYear, setViewYear] = useState(
    value ? parseInt(value.split("-")[0]) : today.getFullYear()
  );
  const [viewMonth, setViewMonth] = useState(
    value ? parseInt(value.split("-")[1]) - 1 : today.getMonth()
  );

  // 연도 선택 페이지 (12개씩)
  const [yearPage, setYearPage] = useState(0);

  const wrapperRef = useRef<HTMLDivElement>(null);
  const [openAbove, setOpenAbove] = useState(false);

  // 외부 클릭 시 닫기
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setOpen(false);
        setView("calendar");
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const handleOpen = () => {
    if (value) {
      const [y, m] = value.split("-").map(Number);
      setViewYear(y);
      setViewMonth(m - 1);
    }
    // 아래 공간 확인 → 부족하면 위로 열기
    if (wrapperRef.current) {
      const rect = wrapperRef.current.getBoundingClientRect();
      const spaceBelow = window.innerHeight - rect.bottom;
      setOpenAbove(spaceBelow < 360);
    }
    setView("calendar");
    setOpen(true);
  };

  // 날짜 선택
  const selectDate = (year: number, month: number, day: number) => {
    const m = String(month + 1).padStart(2, "0");
    const d = String(day).padStart(2, "0");
    onChange(`${year}-${m}-${d}`);
    setOpen(false);
    setView("calendar");
  };

  // 이전/다음 달
  const prevMonth = () => {
    if (viewMonth === 0) {
      setViewYear((y) => y - 1);
      setViewMonth(11);
    } else {
      setViewMonth((m) => m - 1);
    }
  };
  const nextMonth = () => {
    if (viewMonth === 11) {
      setViewYear((y) => y + 1);
      setViewMonth(0);
    } else {
      setViewMonth((m) => m + 1);
    }
  };

  // 달력 셀
  const daysInMonth = new Date(viewYear, viewMonth + 1, 0).getDate();
  const firstDayOfWeek = new Date(viewYear, viewMonth, 1).getDay();
  const daysInPrevMonth = new Date(viewYear, viewMonth, 0).getDate();

  const cells: { day: number; month: number; year: number; isCurrentMonth: boolean }[] = [];

  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    const d = daysInPrevMonth - i;
    const m = viewMonth === 0 ? 11 : viewMonth - 1;
    const y = viewMonth === 0 ? viewYear - 1 : viewYear;
    cells.push({ day: d, month: m, year: y, isCurrentMonth: false });
  }
  for (let d = 1; d <= daysInMonth; d++) {
    cells.push({ day: d, month: viewMonth, year: viewYear, isCurrentMonth: true });
  }
  const remaining = 7 - (cells.length % 7);
  if (remaining < 7) {
    for (let d = 1; d <= remaining; d++) {
      const m = viewMonth === 11 ? 0 : viewMonth + 1;
      const y = viewMonth === 11 ? viewYear + 1 : viewYear;
      cells.push({ day: d, month: m, year: y, isCurrentMonth: false });
    }
  }

  // 선택된 날짜 체크
  const isSelected = (year: number, month: number, day: number) => {
    if (!value) return false;
    const [sy, sm, sd] = value.split("-").map(Number);
    return sy === year && sm === month + 1 && sd === day;
  };

  const isToday = (year: number, month: number, day: number) =>
    year === today.getFullYear() && month === today.getMonth() && day === today.getDate();

  const hasEvent = (year: number, month: number, day: number) => {
    const m = String(month + 1).padStart(2, "0");
    const d = String(day).padStart(2, "0");
    return eventDates.includes(`${year}-${m}-${d}`);
  };

  // 표시 텍스트
  const displayText = value
    ? (() => {
        const [y, m, d] = value.split("-");
        return `${y}년 ${parseInt(m)}월 ${parseInt(d)}일`;
      })()
    : "";

  // 연도 범위
  const currentYearMax = today.getFullYear();
  const minYear = 1920;
  const yearsPerPage = 12;
  const totalPages = Math.ceil((currentYearMax - minYear + 1) / yearsPerPage);

  const openYearView = () => {
    const page = Math.floor((viewYear - minYear) / yearsPerPage);
    setYearPage(Math.max(0, Math.min(page, totalPages - 1)));
    setView("year");
  };

  const getYearsForPage = (page: number) => {
    const start = minYear + page * yearsPerPage;
    const end = Math.min(start + yearsPerPage, currentYearMax + 1);
    const years: number[] = [];
    for (let y = start; y < end; y++) years.push(y);
    return years;
  };

  return (
    <div className="fdp-wrapper" ref={wrapperRef}>
      {/* 입력 버튼 */}
      <button type="button" className="fdp-input" onClick={handleOpen}>
        <span className={displayText ? "fdp-value" : "fdp-placeholder"}>
          {displayText || placeholder}
        </span>
        <svg className="fdp-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
          <path d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1z" />
        </svg>
      </button>

      {/* 드롭다운 달력 */}
      {open && (
        <div className={`fdp-dropdown ${openAbove ? "fdp-above" : ""}`}>
          {view === "calendar" && (
            <>
              <div className="fdp-header">
                <button type="button" className="fdp-nav-btn" onClick={prevMonth}>
                  &lt;
                </button>
                <div className="fdp-header-center">
                  <button type="button" className="fdp-header-btn" onClick={openYearView}>
                    {viewYear}년
                  </button>
                  <button type="button" className="fdp-header-btn" onClick={() => setView("month")}>
                    {viewMonth + 1}월
                  </button>
                </div>
                <button type="button" className="fdp-nav-btn" onClick={nextMonth}>
                  &gt;
                </button>
              </div>

              <div className="fdp-weekdays">
                {WEEKDAYS.map((d) => (
                  <div key={d} className="fdp-weekday">{d}</div>
                ))}
              </div>

              <div className="fdp-days">
                {cells.map((cell, i) => (
                  <button
                    key={i}
                    type="button"
                    className={[
                      "fdp-day",
                      !cell.isCurrentMonth && "other-month",
                      isToday(cell.year, cell.month, cell.day) && "today",
                      isSelected(cell.year, cell.month, cell.day) && "selected",
                      hasEvent(cell.year, cell.month, cell.day) && "has-event",
                    ]
                      .filter(Boolean)
                      .join(" ")}
                    onClick={() => selectDate(cell.year, cell.month, cell.day)}
                  >
                    {cell.day}
                  </button>
                ))}
              </div>
            </>
          )}

          {view === "year" && (
            <>
              <div className="fdp-header">
                <button
                  type="button"
                  className="fdp-nav-btn"
                  onClick={() => setYearPage((p) => Math.max(0, p - 1))}
                  disabled={yearPage === 0}
                >
                  &lt;
                </button>
                <span className="fdp-header-title">연도 선택</span>
                <button
                  type="button"
                  className="fdp-nav-btn"
                  onClick={() => setYearPage((p) => Math.min(totalPages - 1, p + 1))}
                  disabled={yearPage === totalPages - 1}
                >
                  &gt;
                </button>
              </div>
              <div className="fdp-grid">
                {getYearsForPage(yearPage).map((y) => (
                  <button
                    key={y}
                    type="button"
                    className={`fdp-grid-item ${y === viewYear ? "active" : ""}`}
                    onClick={() => {
                      setViewYear(y);
                      setView("month");
                    }}
                  >
                    {y}
                  </button>
                ))}
              </div>
            </>
          )}

          {view === "month" && (
            <>
              <div className="fdp-header">
                <button type="button" className="fdp-nav-btn" onClick={() => setViewYear((y) => y - 1)}>
                  &lt;
                </button>
                <button type="button" className="fdp-header-btn" onClick={openYearView}>
                  {viewYear}년
                </button>
                <button type="button" className="fdp-nav-btn" onClick={() => setViewYear((y) => y + 1)}>
                  &gt;
                </button>
              </div>
              <div className="fdp-grid">
                {MONTHS.map((label, i) => (
                  <button
                    key={i}
                    type="button"
                    className={`fdp-grid-item ${i === viewMonth ? "active" : ""}`}
                    onClick={() => {
                      setViewMonth(i);
                      setView("calendar");
                    }}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
