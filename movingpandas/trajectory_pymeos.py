import pymeos

from .trajectory import Trajectory, DIRECTION_COL_NAME, DISTANCE_COL_NAME, SPEED_COL_NAME, TIMEDELTA_COL_NAME


class PyMEOSTrajectory(Trajectory):

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, df=None, traj_id=None, obj_id=None, t=None, x=None, y=None, crs="epsg:4326", parent=None,
                 pymeos_backend=False, _pymeos_inner: pymeos.TPointSeq = None):
        self.pymeos_backend = True
        if _pymeos_inner is None:
            super(PyMEOSTrajectory, self).__init__(df, traj_id, obj_id, t, x, y, crs, parent)
            self._pymeos_sequence = self._create_pymeos_seq()
        else:
            self._pymeos_sequence = _pymeos_inner
            self.id = traj_id or 1
            self.df = self._pymeos_sequence.to_dataframe()
            self.is_latlon = isinstance(self._pymeos_sequence, pymeos.TGeogPoint)

    def _create_pymeos_seq(self):
        x = list()
        y = list()
        for p in self.df.geometry:
            x.append(p.x)
            y.append(p.y)
        times = self.df.index

        pymeos_seq = pymeos.TPointSeq.from_arrays(times, x, y, None, self.df.crs.to_epsg(), self.is_latlon, True, True,
                                                  pymeos.TInterpolation.LINEAR, False)
        return pymeos_seq

    def _check_timezone_exist(self):
        ts_sample = self.df.index[0]
        return ts_sample.tzinfo is not None and ts_sample.tzinfo.utcoffset(ts_sample) is not None

    def __repr__(self):
        return super().__repr__()

    def size(self):
        return self._pymeos_sequence.num_instants()

    def copy(self):
        return super().copy()

    def to_crs(self, crs):
        return PyMEOSTrajectory(_pymeos_inner=self._pymeos_sequence.set_srid(crs.to_epsg()))

    def get_speed_column_name(self):
        return super().get_speed_column_name()

    def get_distance_column_name(self):
        return super().get_distance_column_name()

    def get_direction_column_name(self):
        return super().get_direction_column_name()

    def get_timedelta_column_name(self):
        return super().get_timedelta_column_name()

    def get_geom_column_name(self):
        return super().get_geom_column_name()

    def to_linestring(self):
        return self._pymeos_sequence.to_shapely_geometry(precision=20)

    def to_linestringm_wkt(self):
        return super().to_linestringm_wkt()

    def to_point_gdf(self):
        return self._pymeos_sequence.to_dataframe().rename_axis('t')

    def to_line_gdf(self):
        return super().to_line_gdf()

    def to_traj_gdf(self, wkt=False):
        return super().to_traj_gdf(wkt)

    def get_start_location(self):
        return self._pymeos_sequence.start_value()

    def get_end_location(self):
        return self._pymeos_sequence.end_value()

    def get_bbox(self):
        box = pymeos.STBox.from_tpoint(self._pymeos_sequence)
        return box.xmin, box.ymin, box.xmax, box.ymax

    def get_start_time(self):
        return super().get_start_time()

    def get_end_time(self):
        return super().get_end_time()

    def get_duration(self):
        return super().get_duration()

    def get_row_at(self, t, method="nearest"):
        return super().get_row_at(t, method)

    def interpolate_position_at(self, t):
        return super().interpolate_position_at(t)

    def get_position_at(self, t, method="interpolated"):
        return super().get_position_at(t, method)

    def get_linestring_between(self, t1, t2, method="interpolated"):
        return super().get_linestring_between(t1, t2, method)

    def get_segment_between(self, t1, t2):
        return super().get_segment_between(t1, t2)

    def _compute_distance(self, row):
        return super()._compute_distance(row)

    def _add_prev_pt(self, force=True):
        super()._add_prev_pt(force)

    def get_length(self):
        return super().get_length()

    def get_direction(self):
        return super().get_direction()

    def get_sampling_interval(self):
        return super().get_sampling_interval()

    def _compute_heading(self, row):
        return super()._compute_heading(row)

    def _compute_speed(self, row):
        return super()._compute_speed(row)

    def _connect_prev_pt_and_geometry(self, row):
        return super()._connect_prev_pt_and_geometry(row)

    def add_traj_id(self, overwrite=False):
        return super().add_traj_id(overwrite)

    def add_direction(self, overwrite=False, name=DIRECTION_COL_NAME):
        return super().add_direction(overwrite, name)

    def add_distance(self, overwrite=False, name=DISTANCE_COL_NAME):
        return super().add_distance(overwrite, name)

    def add_speed(self, overwrite=False, name=SPEED_COL_NAME):
        return super().add_speed(overwrite, name)

    def add_timedelta(self, overwrite=False, name=TIMEDELTA_COL_NAME):
        return super().add_timedelta(overwrite, name)

    def _get_df_with_timedelta(self, name=TIMEDELTA_COL_NAME):
        return super()._get_df_with_timedelta(name)

    def _get_df_with_distance(self, name=DISTANCE_COL_NAME):
        return super()._get_df_with_distance(name)

    def _get_df_with_speed(self, name=SPEED_COL_NAME):
        return super()._get_df_with_speed(name)

    def intersects(self, polygon):
        return super().intersects(polygon)

    def distance(self, other):
        return super().distance(other)

    def hausdorff_distance(self, other):
        return super().hausdorff_distance(other)

    def clip(self, polygon, point_based=False):
        return super().clip(polygon, point_based)

    def intersection(self, feature, point_based=False):
        return super().intersection(feature, point_based)

    def apply_offset_seconds(self, column, offset):
        super().apply_offset_seconds(column, offset)

    def apply_offset_minutes(self, column, offset):
        super().apply_offset_minutes(column, offset)

    def _to_line_df(self):
        return super()._to_line_df()

    def get_mcp(self):
        return super().get_mcp()
