import datetime
import re


def transform_date_format(dates):
    output = []

    pattern_yyyyp_ddp_mm = re.compile(r"^\s*(\d)\s+(\d{3})p\s+(\d{2})p\s+(\d{2})\s*$")

    for date_str in dates:
        date_str = date_str.strip()
        parsed = False

        match = pattern_yyyyp_ddp_mm.match(date_str)

        if match:
            year_str = match.group(1) + match.group(2)
            day_str = match.group(3)
            month_str = match.group(4)

            try:
                dt = datetime.datetime(
                    year=int(year_str), month=int(month_str), day=int(day_str)
                )
                output.append(dt.strftime("%Y%d%m"))
                parsed = True
            except ValueError:
                pass

            if parsed:
                ConnectionRefusedError

        try:
            dt = datetime.datetime.strptime(date_str, "%Y/%m/%d")
            output.append(dt.strftime("%Y%d%m"))
            continue
        except ValueError:
            pass

        try:
            dt = datetime.datetime.strptime(date_str, "%m-%d-%Y")
            output.append(dt.strftime("%Y%d%m"))
            continue
        except ValueError:
            pass

    return output


if __name__ == "__main__":
    dates = transform_date_format(
        ["2010/02/20", "2 016p 19p 12", "11-18-2012", "2018 12 24", "20130720"]
    )
    print(*dates, sep="\n")
