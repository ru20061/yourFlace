"use client";

import { useState } from "react";
import "./calendar.css";

interface CalendarProps {
  selectedDate: Date | null;
  onDateSelect: (date: Date) => void;
  eventDates?: string[];
}

const WEEKDAYS = ["일", "월", "화", "수", "목", "금", "토"];

export default function Calendar({ selectedDate, onDateSelect, eventDates = [] }: CalendarProps) {
  const today = new Date();
  const [currentYear, setCurrentYear] = useState(today.getFullYear());
  const [currentMonth, setCurrentMonth] = useState(today.getMonth());

  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const firstDayOfWeek = new Date(currentYear, currentMonth, 1).getDay();
  const daysInPrevMonth = new Date(currentYear, currentMonth, 0).getDate();

  const prevMonth = () => {
    if (currentMonth === 0) {
      setCurrentYear((y) => y - 1);
      setCurrentMonth(11);
    } else {
      setCurrentMonth((m) => m - 1);
    }
  };

  const nextMonth = () => {
    if (currentMonth === 11) {
      setCurrentYear((y) => y + 1);
      setCurrentMonth(0);
    } else {
      setCurrentMonth((m) => m + 1);
    }
  };

  // 날짜 셀 구성
  const cells: { day: number; isCurrentMonth: boolean; date: Date }[] = [];

  // 이전 달 마지막 날짜들
  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    const d = daysInPrevMonth - i;
    cells.push({ day: d, isCurrentMonth: false, date: new Date(currentYear, currentMonth - 1, d) });
  }

  // 현재 달
  for (let d = 1; d <= daysInMonth; d++) {
    cells.push({ day: d, isCurrentMonth: true, date: new Date(currentYear, currentMonth, d) });
  }

  // 다음 달 시작 날짜들
  const remaining = 7 - (cells.length % 7);
  if (remaining < 7) {
    for (let d = 1; d <= remaining; d++) {
      cells.push({ day: d, isCurrentMonth: false, date: new Date(currentYear, currentMonth + 1, d) });
    }
  }

  const isToday = (date: Date) => date.toDateString() === today.toDateString();
  const isSelected = (date: Date) => selectedDate?.toDateString() === date.toDateString();
  const hasEvent = (date: Date) => {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const d = String(date.getDate()).padStart(2, "0");
    return eventDates.includes(`${y}-${m}-${d}`);
  };

  return (
    <div className="calendar">
      <div className="calendar-header">
        <span className="calendar-month">{currentYear}년 {currentMonth + 1}월</span>
        <div className="calendar-nav">
          <button type="button" onClick={prevMonth}>&lt;</button>
          <button type="button" onClick={nextMonth}>&gt;</button>
        </div>
      </div>
      <div className="calendar-weekdays">
        {WEEKDAYS.map((day) => (
          <div key={day} className="calendar-weekday">{day}</div>
        ))}
      </div>
      <div className="calendar-days">
        {cells.map((cell, idx) => (
          <div
            key={idx}
            className={[
              "calendar-day",
              !cell.isCurrentMonth && "other-month",
              isToday(cell.date) && "today",
              isSelected(cell.date) && "selected",
              hasEvent(cell.date) && "has-event",
            ].filter(Boolean).join(" ")}
            onClick={() => onDateSelect(cell.date)}
          >
            {cell.day}
          </div>
        ))}
      </div>
    </div>
  );
}
